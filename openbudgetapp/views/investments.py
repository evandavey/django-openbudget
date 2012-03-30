from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages


from datetime import *

import pandas as ps
import numpy as np
from pandas.core.datetools import MonthEnd
from openbudgetapp.models import Account,AccountExtra,AccountSet
from decimal import *
import urllib as u
import string

share_data={
    'Alumina':{'code':'AWC.AX'},
    'BHP':{'code':'BHP.AX'},
    'Bluescope':{'code':'BSL.AX'},
    'Commonwealth Bank':{'code':'CBA.AX'},
    'National Australia Bank':{'code':'NAB.AX'},
    'Singtel':{'code':'SGT.AX'},
    'Suncorp':{'code':'SUN.AX'},
    'Telstra':{'code':'TLS.AX'},
    'Wesfarmers':{'code':'WES.AX'},
    'Wesfarmers (N Class)':{'code':'WESN.AX'},
    'Woolworths':{'code':'WOW.AX'},
    'Eldorado':{'code':'EAU.AX'}
}


def sum_accounts(accounts,startdate,enddate,change_sign=False):
    
    account_sum=Decimal(0.0)
    for i in accounts:
        
        ts=i.timeseries
        
        if ts is not None:
            
            try:
                if startdate is None:
                    this_sum=ts[(ts.index<=enddate)].sum()
                else:
                    this_sum=ts[(ts.index>=startdate) & (ts.index<=enddate)].sum()
                
                account_sum+=this_sum
            except:
                pass
                
    if change_sign:
        return account_sum*-1
    else:
        return account_sum
    
def get_share_data(s):
    data = []
    #http://ichart.finance.yahoo.com/table.csv?s=NAB.AX&a=11&b=31&c=2011&d=11&e=31&f=2011&g=d&ignore=.csv

    url = 'http://ichart.finance.yahoo.com/table.csv?s='
    url += s
    #url += "&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv" % (dt.month,dt.day,dt.year,dt.month,dt.day,dt.year)
    f = u.urlopen(url,proxies = {})
    rows = f.readlines()
    for r in rows[1:-1]:
       	values = [x for x in r.split(',')]
	dtstr = datetime.strptime(values[0],'%Y-%m-%d')
       	open = string.atof(values[1])
       	high = string.atof(values[2])
       	low = string.atof(values[3])
       	close = string.atof(values[4])
       	vol = string.atof(values[5])
       	adjclose = string.atof(values[6])
       	data.append([dtstr,open,high,low,close,vol,adjclose])


    return data


def find_share_price(dt,data):   
    close = -1
    for d in data:
	close=d[6]
	if d[0]<=dt:
		break


    return Decimal(close)


@login_required(login_url='/accounts/login')
def report(request,accountset_id,enddate=None,startdate=None,format='html'):
	
	
	accountset=AccountSet.objects.get(pk=accountset_id)
	
	if enddate is None:
		enddate = datetime.today()
	
	else:
		enddate=datetime.strptime(enddate,'%Y%m%d')
	
	enddate=enddate-MonthEnd()
	
	if startdate is None:
		startdate = (enddate-3*MonthEnd())+timedelta(days=1)
	else:
		startdate=datetime.strptime(startdate,'%Y%m%d')
	
	
	
	data={
	    'income':sum_accounts(Account.objects.filter(account_type='INCOME',accountset=accountset),startdate,enddate,True),
	    'expenses':sum_accounts(Account.objects.filter(account_type='EXPENSE',accountset=accountset),startdate,enddate),
	    'liabilities_start':sum_accounts(Account.objects.filter(account_type='LIABILITY',accountset=accountset),None,startdate,True),
	    'liabilities_end':sum_accounts(Account.objects.filter(account_type='LIABILITY',accountset=accountset),None,enddate,True),
	    'liabilities_yearstart':sum_accounts(Account.objects.filter(account_type='LIABILITY',accountset=accountset),None,datetime(enddate.year,1,1),True),
	    'income_ytd':sum_accounts(Account.objects.filter(account_type='INCOME',accountset=accountset),datetime(enddate.year,1,1),enddate,True),
    	'expenses_ytd':sum_accounts(Account.objects.filter(account_type='EXPENSE',accountset=accountset),datetime(enddate.year,1,1),enddate),
	    'contributions':sum_accounts(Account.objects.filter(account_type='EQUITY',accountset=accountset),startdate,enddate,True),
	    'contributions_ytd':sum_accounts(Account.objects.filter(account_type='EQUITY',accountset=accountset),datetime(enddate.year,1,1),enddate,True),
	}
	
	"""
	Interest Bearing Accounts
	"""
	
	ib=Account.objects.filter(accountextra__investment_category='INTEREST-BEARING',accountset=accountset)
	
	i_data=[]
	for i in ib.filter(account_type='BANK'):
	    print 'calculating interest for %s' % i.name
	    start=sum_accounts([i],None,startdate)
	    end=sum_accounts([i],None,enddate)

        
	    interest=i.split_set.filter(tx__description__icontains='Interest',accountset=accountset).timeseries()
	    try:
	        interest=interest[(interest.index>startdate+timedelta(days=5)) & (interest.index<enddate+timedelta(days=5))].sum()
	        r=float(interest)/float(start)
	    except:
	        import sys
	        print '...error calculating %s' % sys.exc_info()[1] 
	        r=0
	    if r:
	        print '...effective rate %.2f' % r
	        i_data.append({'account':i.name,'interest':interest,'rate':r*400,'start':start,'end':end})
	    

   
	
	ib_data={
	    'income':sum_accounts(ib.filter(account_type='INCOME',accountset=accountset),startdate,enddate,True),
	    'expenses':sum_accounts(ib.filter(account_type='EXPENSE',accountset=accountset),startdate,enddate),
	    'end':sum_accounts(ib.filter(account_type='BANK',accountset=accountset),None,enddate),
	    'start':sum_accounts(ib.filter(account_type='BANK',accountset=accountset),None,startdate),
	    'yearstart':sum_accounts(ib.filter(account_type='BANK',accountset=accountset),None,datetime(enddate.year,1,1)),
	 
	    
	}
	
	ib_data['net']=ib_data['income']-ib_data['expenses']
	ib_data['return']=((ib_data['net']/ib_data['start']))*100
	ib_data['return_pa']=ib_data['return']*4
	
	for x in i_data:
	    x['Ws']=(x['end']/ib_data['end'])*100
        

	"""
	Share Accounts
	"""
	
	s=Account.objects.filter(accountextra__investment_category='STOCK',accountset=accountset)
	
	s_end=Decimal(0)
	s_start=Decimal(0)
	s_yearstart=Decimal(0)
    
	for h in Account.objects.filter(account_type='STOCK',accountset=accountset):
	    
	    print 'Revaluing %s at %s and %s' % (h.name,startdate,enddate)
	    
	    try:

	        code=share_data[h.name]['code']
	        share_data[h.name]['h_yearstart']=sum_accounts([h],None,datetime(enddate.year,1,1))    
	        share_data[h.name]['h_end']=sum_accounts([h],None,enddate)
	        share_data[h.name]['h_start']=sum_accounts([h],None,startdate)
	        price_data=get_share_data(code)
	        share_data[h.name]['p_end']=find_share_price(enddate,price_data)
	        share_data[h.name]['p_start']=find_share_price(startdate,price_data)
	        share_data[h.name]['p_yearstart']=find_share_price(datetime(enddate.year,1,1),price_data)

	        share_data[h.name]['p_change']=share_data[h.name]['p_end']-share_data[h.name]['p_start']
	        share_data[h.name]['p_return']=(share_data[h.name]['p_change']/share_data[h.name]['p_start'])*100
	        s_start+=share_data[h.name]['p_start']*share_data[h.name]['h_start']
	        s_end+=share_data[h.name]['p_end']*share_data[h.name]['h_end']
	        s_yearstart+=share_data[h.name]['p_yearstart']*share_data[h.name]['h_yearstart']
	        
	    except:
	        messages.add_message(request, messages.WARNING, 'Error revaluing %s' % h.name)
	        pass
	        
	for k,x in share_data.iteritems():
	    print k
	    x['MV']=x['p_end']*x['h_end']
	    x['Wp']=(x['MV'] / s_end)*100
	    x['Rp']=(x['Wp']/100)*x['p_return']
        
        
    
	s_data={
	    'income':sum_accounts(s.filter(account_type='INCOME',accountset=accountset),startdate,enddate,True),
	    'expenses':sum_accounts(s.filter(account_type='EXPENSE',accountset=accountset),startdate,enddate),
	    'income_ytd':sum_accounts(s.filter(account_type='INCOME',accountset=accountset),datetime(enddate.year,1,1),enddate,True),
    	'expenses_ytd':sum_accounts(s.filter(account_type='EXPENSE',accountset=accountset),datetime(enddate.year,1,1),enddate),
	    'end':s_end,
	    'start':s_start,
	    'yearstart':s_yearstart,
	}
	
	s_data['net']=s_data['income']-s_data['expenses']
	s_data['net_ytd']=s_data['income_ytd']-s_data['expenses_ytd']
	s_data['return']=((s_data['net']/s_data['start']))*100
	s_data['return_pa']=s_data['return']*4
	s_data['change']=s_end-s_start
	s_data['change_ytd']=s_end-s_yearstart
	s_data['p_return']=((s_data['change']/s_data['start']))*100
	s_data['p_return_ytd']=((s_data['change_ytd']/s_data['yearstart']))*100
	s_data['total_return_ytd']=(((s_data['change_ytd']+s_data['net_ytd'])/s_data['yearstart']))*100

	"""
	Pension Accounts
	"""
	
	p=Account.objects.filter(accountextra__investment_category='PENSION',accountset=accountset)
	
	
	p_data={
	    'income':sum_accounts(p.filter(account_type='INCOME'),startdate,enddate,True),
	    'expenses':sum_accounts(p.filter(account_type='EXPENSE'),startdate,enddate),
	    'end':sum_accounts(p.filter(account_type='ASSET'),None,enddate),
	    'start':sum_accounts(p.filter(account_type='ASSET'),None,startdate),
	    'yearstart':sum_accounts(p.filter(account_type='ASSET'),None,datetime(enddate.year,1,1)),
	    
	}
	
	p_data['net']=p_data['income']-p_data['expenses']
	p_data['return']=((p_data['net']/p_data['start']))*100
	p_data['return_pa']=p_data['return']*4
	
	total_start=ib_data['start']+s_data['start']+p_data['start']
	total_end=ib_data['end']+s_data['end']+p_data['end']
	total_yearstart=ib_data['yearstart']+s_data['yearstart']+p_data['yearstart']
	data['equity_end']=total_end-data['liabilities_end']
	data['equity_start']=total_start-data['liabilities_start']
	data['equity_yearstart']=total_yearstart-data['liabilities_yearstart']
	
	data['roe']=(((data['equity_end']-data['contributions'])/data['equity_start'])-1)*100
	data['roe_pa']=data['roe']*4
	data['roe_ytd']=(((data['equity_end']-data['contributions_ytd'])/data['equity_yearstart'])-1)*100
	
	data['income_net']=data['income']-data['expenses']
	data['income_net_ytd']=data['income_ytd']-data['expenses_ytd']
	
	aa_data=[
	{
        'label': 'Australian Cash',
        'val1': ib_data['start'],
        'val2': ib_data['end'],
        'weight1': (ib_data['start']/total_start)*100,
        'weight2':(ib_data['end']/total_end)*100,
    
    },
    {
         'label': 'Australian Listed Equities',
         'val1': s_data['start'],
         'val2': s_data['end'],
         'weight1': (s_data['start']/total_start)*100,
         'weight2':(s_data['end']/total_end)*100,

     },
    {
        'label': 'Australian Pensions',
        'val1': p_data['start'],
        'val2': p_data['end'],
        'weight1': (p_data['start']/total_start)*100,
        'weight2':(p_data['end']/total_end)*100,
    
    },
    ]
    

	
	ct={'end_dt':enddate,
		'start_dt':startdate,
		'ib_data':ib_data,
		's_data':s_data,
		'p_data':p_data,
		'data':data,
		'aa_data':aa_data,
		'share_data':share_data,
		'i_data':i_data,
	
	
	}
	
	
	"""
	Template is in markdown format so we need to render it then convert to html
	"""
	
	import subprocess

	markdown=render_to_string('openbudgetapp/investments/report.md',ct,context_instance=RequestContext(request))
	
	if format=='md':
	    #Just return the rendered markdown template
	    response = HttpResponse(mimetype='application/txt')
	    response['Content-Disposition'] = 'attachment; filename=report.md'
	    response.write(markdown)
	    return response
	    
	else:
	    #Convert the template to html for site display
	    #requires multimarkdown installed on host system (on osx using Homebrew: brew install multimarkdown)
	    process = subprocess.Popen(['/usr/local/bin/multimarkdown'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	
    	process.stdin.write(markdown)
	
    	report_html=process.communicate()[0]
    	
        from BeautifulSoup import BeautifulSoup   
        
        soup=BeautifulSoup(report_html)
        
        report_html=str(soup.body)
        report_html=report_html.replace('<body>','').replace('</body>','')
         	
    	report_html='<div id="investment-report">'+report_html+'</div>'
	
    	ct={'html':report_html,
		
    	}
	
    	return render_to_response('openbudgetapp/investments/report.html',ct,context_instance=RequestContext(request))
	
	
    