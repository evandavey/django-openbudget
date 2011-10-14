from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from openbudgetapp.models import Account
from datetime import *
from dateutil.relativedelta import relativedelta

@login_required(login_url='/accounts/login/')
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)

def get_account_nav(request,accounts=None,maxdepth=99,currdepth=1):
	"""Recursively build a list of product categories. The resulting list is meant to be iterated over in a view"""
	
	if accounts==None:
		accounts= Account.objects.filter(parent=None)
		
	else:
		yield 'in'

	
	for account in accounts:
	
		yield account
		subaccounts = Account.objects.select_related().filter(parent=account)
	
		account.depth=currdepth
		if len(subaccounts) and (currdepth+1)<=maxdepth:
			account.leaf=False
			currdepth+=1
			for x in get_account_nav(request,subaccounts,maxdepth,currdepth):
				if x=='out':
					currdepth-=1
				yield x
		else:
			account.leaf=True
	
	yield 'out'
	


def index(request):
	
	iqs=Account.objects.filter(account_type='INCOME',parent__name='Income').order_by('name')
	eqs=Account.objects.filter(account_type='EXPENSE',parent__name='Expenses').order_by('name')	
	
	startdate=datetime(2011,1,1)
	numperiods=12
	freq='m'
	depth=1
	
	dates=[]
	startdates=[]
	startdt=startdate
	for i in range(0,numperiods):
		startdates.append(startdt)
		enddt=startdt+relativedelta(months=+1)+relativedelta(days=-1)
	
		dates.append(enddt)
		startdt=enddt+relativedelta(days=1)
		
	
			
	income_list=list(get_account_nav(request,iqs,depth))
	expense_list=list(get_account_nav(request,eqs,depth))
	
	account_type_list=[{'label':'INCOME','list':income_list},{'label':'EXPENSES','list':expense_list}]
	
	for a in account_type_list:

		for i in a['list']:
			if type(i) != str:
				i.budget_data={}
			
				for x in range(0,len(dates)):
					
					
						istartdate=startdates[x].date()
						ienddate=dates[x].date()
						print "Calculating budget&actual for %s,%s,%s" % (i,istartdate,ienddate)
						actual=i.balance_between(istartdate,ienddate,True)
						
						#pass in global start date
						budgeted=round(i.budget_between(istartdate,ienddate,startdate.date()),0)
						
						i.budget_data[ienddate]={'actual': actual, 'budget':budgeted,'vsbudget':float(budgeted)-float(actual)}
	
		
	ct={'account_type_list':account_type_list,
		'dates': dates,
	
	}
	return render_to_response('index.html',ct,context_instance=RequestContext(request))
	
	
