from datetime import *
from openbudgetapp.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import pandas as ps
from pandas.core.datetools import MonthEnd


@login_required(login_url='/accounts/login/')
def income_expense_analysis(request,accountset_id):


    account_type='EXPENSE'
    
    startdate=datetime(2011,12,31)
    enddate=datetime(2012,3,31)
    
    method='m'
    
    #load the budget panel
    accounts=Account.objects.filter(account_type=account_type,accountset_id=accountset_id)


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
        
        
    return render_to_response('openbudgetapp/reports/income_expense_analysis/pie.html',ct,context_instance=RequestContext(request))
    
        
        
        
    