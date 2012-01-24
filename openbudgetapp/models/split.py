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
        
        #note: this can contain duplicate dates
        df=ps.DataFrame(r,index=list(vldt))
        
        
        #group by date,investment and portfolio to aggregate  **remove portfolio to overcome group portfolio issues
        df=df.groupby(lambda x: datetime(x.year,x.month,x.day)).sum()
               
       
                    
        ts=ps.TimeSeries(df['value'],index=df.index)
        
        return ts

class SplitManager(models.Manager):
    def get_query_set(self):
        return SplitQuerySet(self.model)


class Split(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'


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
	def description(self):
		return self.tx.description
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s %s %.2f" % (self.date,self.account_name,self.value) 
