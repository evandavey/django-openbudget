from django.db import models
import pandas as ps
import numpy as np
from django.db.models.query import QuerySet
from datetime import datetime


class SplitQuerySet(QuerySet):
    """
    A queryset object that contains a date field for conversion into a pandas data frame
    """
    
    def timeseries(self):
        
        qs=self
        
        if len(qs)==0:
            return None

        dates=list(qs.dates('tx__postdate','day'))
  
        vlqs = qs.values_list()
        vldt = qs.values_list('tx__postdate',flat=True)
        
        
              
        r = np.core.records.fromrecords(vlqs, names=[f.name for f in self.model._meta.fields])


        
        #print [f.name for f in self.model._meta.fields]
        
        #note: this can contain duplicate dates
        df=ps.DataFrame(r,index=list(vldt))
        df=df['value']
        
        df=df.groupby(lambda x: datetime(x.year,x.month,x.day)).sum()
        ts=ps.TimeSeries(df,index=df.index)
        #print ts
        return ts

class SplitManager(models.Manager):
    def get_query_set(self):
        return SplitQuerySet(self.model)


class Split(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'
		
	accountset=models.ForeignKey("AccountSet")

	guid=models.CharField(max_length=32,primary_key=True)
	tx=models.ForeignKey("Transaction")
	account=models.ForeignKey("Account")
	value=models.DecimalField(decimal_places=4,max_digits=20)
	
	objects=SplitManager()
	    
	
	@property
	def date(self):
		return self.tx.postdate
		
	@property
	def account_name(self):
		return self.account.name
		
	@property
	def db_or_cr(self):
	    
	    if self.account.account_type=='EXPENSE':
	        if self.value>0:
	            return "DB"
	        else: 
	            return "CR"
	    else:
	        if self.value<0:
	            return "CR"
	        else: 
	            return "DB"
	            
	            
	@property
	def amt(self):
	    return abs(self.value)
	
	@property
	def description(self):
		return self.tx.description
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s %s (%s) %.2f" % (self.date,self.account_name,self.account.account_type,abs(self.value)) 
