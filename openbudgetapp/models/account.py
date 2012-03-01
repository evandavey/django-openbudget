from django.db import models
from django.db.models.query import QuerySet
from openbudgetapp.models.split import Split
from openbudgetapp.models.accountbudget import AccountBudget
from openbudgetapp.models.inflationrate import InflationRate

import numpy as np
import pandas as ps
from decimal import *
from datetime import datetime,time

class AccountQuerySet(QuerySet):
    def budgetpanel(self,startdate,enddate):

        analysis_dates=ps.DateRange(startdate,enddate,offset=ps.DateOffset(days=1))

        data={}
        for a in self:
            if type(a) != str:

                df=a.dataframe

                if df is not None:
                    df=df.reindex(analysis_dates)
                    data[a]=df

        p=ps.Panel(data,major_axis=analysis_dates)

        return p

class AccountManager(models.Manager):
    
    def get_query_set(self):
          return AccountQuerySet(self.model)
    
   
    


class Account(models.Model):

    class Meta:
        app_label = 'openbudgetapp'
        ordering = ['name']


    accountset=models.ForeignKey("AccountSet")
    guid=models.CharField(max_length=32,primary_key=True)
    name=models.CharField(max_length=2048)
    account_type=models.CharField(max_length=2048)
    parent=models.ForeignKey('self',null=True,related_name='child')
    objects=AccountManager()
    code=models.CharField(max_length=20,null=True)

    @property
    def extras(self):

        extras=self.accountextra_set.all()

        if extras:
            return extras[0]
        else:
            return None

    @property
    def inflationrate(self):

        extras=self.extras
        if not extras:
            return 0


        ir=InflationRate.objects.filter(category=extras.inflation_category).order_by('enddate')


        if ir:
            return ir[0].rate
        else:
            return 0


    @property
    def timeseries(self):

        return self.split_set.all().timeseries()


    @property 
    def depth(self):
    
        depth=0
        p=self.parent
        while p is not None:
            p=p.parent
            depth+=1
            
        return depth
            

    @property
    def formatted_name(self):

        names=[]
        parent=self.parent
        if parent is not None:
            while parent.name != 'Root Account' and parent.name.upper() != self.account_type + 'S':
                names.append(parent.name)
                parent=parent.parent

        name=''

        names.reverse()
        for n in names:
            name+=n+":"

        return name+':'+self.name


    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return "%s (%s)" % (self.formatted_name,self.account_type)



    @property
    def investment_category(self):
        
        e=self.accountextra_set.all()
        
        if e:
            return e[0].investment_category
        else:
            return "NONE"

    def splits(self,startdate=None,enddate=None):

        if startdate is None or enddate is None:
            qs=Split.objects.filter(account=self)
        else:
            qs=Split.objects.filter(account=self,tx__postdate__lte=enddate,tx__postdate__gte=startdate)

        if len(qs)==0:
            return None

        vlqs = qs.values_list()
        splits = np.core.records.fromrecords(vlqs, names=[f.name for f in Split._meta.fields])

        return splits


    def balance_between(self,startdate=None,enddate=None,includeChildren=False):


        splits=self.splits(startdate,enddate)

        if splits is None:
            bal=0
        else:
            bal=splits.value.sum()

        if includeChildren:

            for c in self.child.all():
                bal+=c.balance_between(startdate,enddate,includeChildren)


        return bal


    @property
    def balance(self):

        splits=self.splits()

        if splits is None:
            bal=0
        else:
            bal=splits.value.sum()

        bal+=self.child_balance

        return bal


    @property
    def child_balance(self):


        bal=0
        for c in self.child.all():
            #print "%s %f" % (c,c.balance)

            bal+=c.balance

        return bal

    @property
    def budgets(self):


        bs=self.accountbudget_set.all()

        for c in self.child.all():
            bs = bs | c.budgets

        return bs

    @property
    def dataframe(self):

        bs=self.budgets
        ts=self.timeseries
        
        if len(ts)==0:
            return None

        for c in self.child.all():
            cts=c.timeseries
            if cts:
                ts=ts.combine(cts,np.sum,0)

        if bs:
            bts=bs[0].timeseries
            if len(bs)>1:
                for b in range(1,len(bs)):
                    bts=bts.combine(b.timeseries,np.sum,0)
        else:
            bts=ps.TimeSeries([0],index=[ts.index[0]])

        startdate=min(ts.index[0],bts.index[0])
        enddate=max(ts.index[-1],bts.index[-1])

        dates=ps.DateRange(startdate,enddate,offset=ps.DateOffset(days=1))


        
        bts=bts.reindex(dates)
        ts=ts.reindex(dates)


        df=ps.DataFrame({'actual':ts,'budget':bts})
        df=df.fillna(0)
        df['actual']=df['actual'].apply(Decimal)
        df['budget']=df['budget'].apply(Decimal)
        df['vsbudget']=(df['actual']-df['budget']).apply(Decimal)
        
        types=[]
        accounts=[]
        depth=[]
        for dt in df.index:
            types.append(self.account_type)
            accounts.append(self.guid)
            depth.append(self.depth)
       
        edf=ps.DataFrame({'type':types,'account':accounts,'depth':depth},index=df.index)
        
        df['type']=edf['type']
        df['account']=edf['account']
        df['depth']=edf['depth']
        
        return df


    def budget_between(self,startdate,enddate,global_startdate=None):

        #all budget items with a start date greater than now
        from django.db.models import Q


        if global_startdate is None:
            b_qs=AccountBudget.objects.filter(startdate__gte=startdate,account=self).exclude(startdate__gt=enddate)
        else:
            print "global start %s" % global_startdate
            b_qs=AccountBudget.objects.filter(startdate__gte=global_startdate,enddate__gt=startdate,account=self).exclude(startdate__gt=enddate)

        print "Found %s budgets in range %s to %s for %s" % (len(b_qs),startdate,enddate,self)

        budget=0
        for b in b_qs:

            if b.enddate <= enddate:
                budget+=float(b.value)

            #allocate an ammount of the budget
            else:
                b_days=float((b.enddate-b.startdate).days)
                p_days=float((enddate-startdate).days)

                scale=p_days/b_days

                #print "B=%f,P=%f,Scale: %f" % (b_days,p_days,scale)

                budget+=round(float(b.value)*scale,2)


        for c in self.child.all():
            budget+=c.budget_between(startdate,enddate,global_startdate)

        return budget
