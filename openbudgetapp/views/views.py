from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from openbudgetapp.models import Account
from datetime import *
from dateutil.relativedelta import relativedelta
import pandas as ps
import numpy as np
from pandas.core.datetools import MonthEnd
from decimal import Decimal

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
	


def index(request,startdate=datetime(2011,6,1),enddate=datetime(2011,12,31),depth=3,method='m',threshold=-5):
	
	iqs=Account.objects.filter(account_type='INCOME',parent__name='Income').order_by('name')
	eqs=Account.objects.filter(account_type='EXPENSE',parent__name='Expenses').order_by('name')	

	depth=int(depth)

	print "method: %s,depth %d" % (method,depth)
				
	income_list=list(get_account_nav(request,iqs,depth))
	expense_list=list(get_account_nav(request,eqs,depth))
	
	account_type_list=[{'type':'I','label':'INCOME','list':income_list},{'type':'E','label':'EXPENSES','list':expense_list}]
	
	analysis_dates=ps.DateRange(startdate,enddate,offset=ps.DateOffset(days=1))
	dates=[]
	running_budget=Decimal(0)
	running_actual=Decimal(0)
	
	data={}
	for a in expense_list:
	    if type(a) != str:
	        
	        df=a.dataframe
	        
	        if df is not None:
	            df=df.reindex(analysis_dates)
	            data[a]=df
	    
	p=ps.Panel(data,major_axis=analysis_dates)
	
	print p
	
	for a in account_type_list:
		totals={}
		for i in a['list']:
			budget_data=[]
			if type(i) != str:
				
				df=i.dataframe
				
				if df:
				    df=df.reindex(analysis_dates)
				
				else:
				    continue
				
				
				#group the data frame for analysis
				
				if method=='m':
					grouped=df.groupby(lambda x: datetime(x.year,x.month,1)+MonthEnd())
				elif method=='q':
					grouped=df.groupby(lambda x: datetime(x.year,(((x.month-1)//3)+1)*3,1)+MonthEnd())
				else:
					grouped=df.groupby(lambda x: datetime(x.year,12,31))
				
			
				if len(dates)==0:
					dates=sorted(grouped.groups.iterkeys())
				
						
					
				for (g,d) in grouped:
					budget=round(d.budget.sum(),0)
					actual=round(float(d.actual.sum()),0)
					vsbudget=budget-float(actual)
					
					try:
						totals[g]['budget']+=budget
						totals[g]['actual']+=actual
					except:
						totals[g]={'budget':budget,'actual':actual}
						
					
					budget_data.append({'budget':budget,'actual':actual,'vsbudget':vsbudget})
				
				running_budget+=Decimal(df['budget'].sum())
				running_actual+=Decimal(df['actual'].sum())
				
				i.budget_sums={'vsbudget':round(float(df['actual'].sum())-float(df['budget'].sum()),0),'budget':round(df['budget'].sum(),0),'actual':round(float(df['actual'].sum()),0)}
				i.budget_data=budget_data
				#print grouped.sum()
		
		#sorting hack
		a['totals']=[]
		for d in dates:
			actual=totals[d]['actual']
			budget=totals[d]['budget']
			
			a['totals'].append({'budget':budget,'actual':actual,'vsbudget':actual-budget})
			
		a['budget_sums']={'vsbudget':round(float(running_actual)-float(running_budget),0),'budget':round(running_budget,0),'actual':round(float(running_actual),0)}
	
		
	summary_totals=[]
	for i in range(0,len(dates)):
		summary_totals.append({'budget':0,'actual':0,'vsbudget':0})
	
	for a in account_type_list:
		i=0
	
		for t in a['totals']:
			if a['type']=='I':
				summary_totals[i]['budget']+=t['budget']
				summary_totals[i]['actual']+=t['actual']	
			else:
			
				summary_totals[i]['budget']-=t['budget']
				summary_totals[i]['actual']-=t['actual']
				
			summary_totals[i]['vsbudget']=summary_totals[i]['actual']-summary_totals[i]['budget']
			i+=1
			
	summary_overall_total={'budget':0,'actual':0,'vsbudget':0}

	for s in summary_totals:
		summary_overall_total['budget']+=s['budget']
		summary_overall_total['actual']+=s['actual']
		summary_overall_total['vsbudget']+=s['actual']-s['budget']
		
		
	ct={'account_type_list':account_type_list,
		'dates': dates,
		'summary_totals': summary_totals,
		'summary_overall_total':summary_overall_total,
		'threshold_over': threshold,
		'threshold_under': -1*threshold,
	
	
	}
	return render_to_response('index.html',ct,context_instance=RequestContext(request))
	
	
	
	

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
	
    
        
    
    
        
        
    

    
    

