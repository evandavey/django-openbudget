from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from openbudgetapp.models import Account,AccountSet
from datetime import *
from dateutil.relativedelta import relativedelta
import pandas as ps
import numpy as np
from pandas.core.datetools import MonthEnd
from decimal import Decimal
from django.shortcuts import redirect


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')
    


@login_required(login_url='/accounts/login/')
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)

def get_account_nav(accounts=None,maxdepth=99,currdepth=1):
	"""Recursively build a list of product categories. The resulting list is meant to be iterated over in a view"""
	
	if accounts==None:
		accounts= Account.objects.filter(parent=None)
		
	else:
	    pass
		#yield 'in'

	
	for account in accounts:
	
		yield account
		subaccounts = Account.objects.select_related().filter(parent=account)
	
		account.depth=currdepth
		if len(subaccounts) and (currdepth+1)<=maxdepth:
			account.leaf=False
			currdepth+=1
			for x in get_account_nav(subaccounts,maxdepth,currdepth):
				if x=='out':
					currdepth-=1
				yield x
		else:
			account.leaf=True
	
	#yield 'out'

def budget_df(account,startdate=datetime(2011,1,1),enddate=datetime(2011,12,31)):
	

	analysis_dates=ps.DateRange(startdate,enddate,offset=ps.DateOffset(days=1))

  
    
    

	print "loading df %s" % account.name

	budgets=account.budgets

	b_ts=None
	#add budgets together
	for b in budgets:

		this_ts=b.timeseries.reindex(index=analysis_dates,method=None)

		if b_ts is None:
			b_ts=this_ts
		else:
			b_ts+=this_ts

	#handle case where account has no budgets
	if b_ts is None:
		b_ts_values=[Decimal(0) for x in analysis_dates]
	else:
		b_ts_values=b_ts.values

	#reindex the account timeseries to the analysis period		
	a_ts=account.timeseries
	
	for child in account.child.all():
		
		child_ts=child.timeseries
		if child_ts is None:
			continue
		else:
			child_ts=child_ts.reindex(index=analysis_dates,method=None)
			if a_ts is None:
				a_ts=child_ts.fillna(Decimal(0))
			else:
				a_ts+=child_ts.fillna(Decimal(0))
	

	#handle case where account has no transactions
	if a_ts is None:
		a_ts_values=[Decimal(0) for x in analysis_dates]
	else:
		a_ts=a_ts.reindex(index=analysis_dates,method=None)
		a_ts_values=a_ts.values


	df=ps.DataFrame({'actual':a_ts_values,'budget':b_ts_values},index=analysis_dates)

	#convert NaN to zeros and data to type Decimal
	df=df.applymap(float).applymap(np.nan_to_num).applymap(Decimal)

	df['vsbudget']=df['actual']-df['budget']

	
	
	
	return df
	


def index(request):
	
    from openbudgetapp.forms import AccountSetForm
    
    accountsets=None
    for g in request.user.groups.all():
        if accountsets is None:
            accountsets=g.accountset_set.all()
        else:
            accountsets = accountsets | g.accountset_set.all()
        
    
    if request.method == 'POST': # If the form has been submitted...
        form = AccountSetForm(accountsets,request.POST) # A form bound to the POST data
        
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            accset=form.cleaned_data['accountset']
            
            ct={'form':form,'accountset':accset}
            return render_to_response('index.html',ct,context_instance=RequestContext(request))
            
    else:
        form = AccountSetForm(accountsets) # An unbound form

    if accountsets:
        accset=accountsets[0]
    else:
        accset=None
        form=None
        
    ct={'form':form,'accountset':accset}
    return render_to_response('openbudgetapp/index.html',ct,context_instance=RequestContext(request))
    
    

	
	
	
	

def budget_report(request,startdate=datetime(2011,6,1),enddate=datetime(2011,12,31),depth=3,method='m',threshold=-5):
    

    
    #load the budget panel
    accounts=Account.objects.filter(account_type='EXPENSE')
    
    
    p=accounts.budgetpanel(startdate,enddate)
    
    
    #group the panel into analysis subperiods
    if method=='m':
        grouped=p.groupby(lambda x: datetime(x.year,x.month,1)+MonthEnd())
    elif method=='q':
        grouped=p.groupby(lambda x: datetime(x.year,(((x.month-1)//3)+1)*3,1)+MonthEnd())
    else:
        grouped=p.groupby(lambda x: datetime(x.year,12,31))
        
 
    
    group_labels=[]
   
    from django.utils.datastructures import SortedDict
    data=SortedDict()
    data['total']=SortedDict()
    
    
    for (g,gp) in grouped:
        group_labels.append(g)
       
        for i in gp:
            act=gp[i]['actual'].fillna(0).sum()
            bud=gp[i]['budget'].fillna(0).sum()
            
            try:
                data[i][g]={'actual':act,'budget':bud}
                data[i]['total']['actual']+=act
                data[i]['total']['budget']+=bud
            except:
                data[i]=SortedDict()
                data[i][g]={'actual':act,'budget':bud}
                data[i]['total']={'actual':act,'budget':bud}
                
                     
        
        data['total'][g]={
            'actual':gp.minor_xs('actual').fillna(0).sum().sum(),
            'budget':gp.minor_xs('budget').fillna(0).sum().sum(),
        }
     
    data['total']['total']={
        'actual': p.minor_xs('actual').fillna(0).sum().sum(),
        'budget': p.minor_xs('budget').fillna(0).sum().sum(),
    }
        
    ct={
        'group_labels': group_labels,
        'data': data,
    
    }
    
    return render_to_response('budgetreport.html',ct,context_instance=RequestContext(request))
	
    
        
    
    
        
        
    

    
    

