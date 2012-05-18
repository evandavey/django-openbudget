from datetime import *
from openbudgetapp.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import pandas as ps
from pandas.core.datetools import MonthEnd
from django.utils.datastructures import SortedDict



def budget_data(accounts,startdate,enddate,method):


    p=accounts.budgetpanel(startdate,enddate)


    #group the panel into analysis subperiods
    if method=='m':
        grouped=p.groupby(lambda x: datetime(x.year,x.month,1)+MonthEnd())
    elif method=='q':
        grouped=p.groupby(lambda x: datetime(x.year,(((x.month-1)//3)+1)*3,1)+MonthEnd())
    else:
        grouped=p.groupby(lambda x: datetime(x.year,12,31))
      
      
    group_labels=[]

    data=SortedDict()
    data['total']=SortedDict()  
    
    #calculate overall period totals
    data['total']['total']={
        'actual': p.minor_xs('actual').fillna(0).sum().sum(),
        'budget': p.minor_xs('budget').fillna(0).sum().sum(),
    }
    
    for (g,gp) in grouped:
        group_labels.append(g)
        
        #calculate subperiod totals
        data['total'][g]={
            'actual':gp.minor_xs('actual').fillna(0).sum().sum(),
            'budget':gp.minor_xs('budget').fillna(0).sum().sum(),
        }
        
        for i in gp:
            act=gp[i]['actual'].fillna(0).sum()
            bud=gp[i]['budget'].fillna(0).sum()
            
            act_tot=float(data['total'][g]['actual'])
            bud_tot=float(data['total'][g]['budget'])
            
            if act_tot:
                act_pct=float(act)/act_tot
            else:
                act_pct=0
                
            if bud_tot:
                bud_pct=float(act)/bud_tot
            else:
                bud_pct=0
            
            try:
                data[i][g]={
                            'actual':act,
                            'budget':bud,
                            'actual_pct':act_pct,
                            'budget_pct':bud_pct,
                }
                
                #category total for period
                data[i]['total']['actual']+=act
                data[i]['total']['budget']+=bud
            except:
                data[i]=SortedDict()
                data[i][g]={
                            'actual':act,
                            'budget':bud,
                            'actual_pct':act_pct,
                            'budget_pct':bud_pct,
                }
                
                
                data[i]['total']={'actual':act,'budget':bud}
                
                
        return (data,group_labels)


@login_required(login_url='/accounts/login/')
def income_expense_analysis(request,accountset_id):


    account_type='EXPENSE'
    
    startdate=datetime(2011,12,1)
    enddate=datetime(2012,3,31)
    
    method='m'
    
    #load the budget panel
    accounts=Account.objects.filter(account_type=account_type,accountset_id=accountset_id)

    data,group_labels=budget_data(accounts,startdate,enddate,method)

    #convert data into overall %
    
    data={}
    for l,a in data.iteritems():
        data[l]=a['total']['actual']
        data['testing']=1
        
    
    
    ct={
        'data': data,
        'name': 'Breakdown By Account',

    }
        
        
    return render_to_response('openbudgetapp/reports/income_expense_analysis/pie.html',ct,context_instance=RequestContext(request))
    
        
        
        
    