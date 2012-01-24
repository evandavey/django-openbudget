from django.db import models
from openbudgetapp.models.split import Split
import pandas as ps
from decimal import Decimal
from django.db.models.query import QuerySet



  
class AccountBudget(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'
		


	account=models.ForeignKey("Account")
	value=models.DecimalField(decimal_places=4,max_digits=20)
	startdate=models.DateField()
	enddate=models.DateField()
	note=models.TextField(null=True,blank=True)
	estimated=models.BooleanField(default=True)
	pctnondiscrentionary=models.FloatField(default=1.00,verbose_name='Non Discrentionary %')

	    	    
	
	@property
	def timeseries(self):
		dates=ps.DateRange(str(self.startdate),str(self.enddate),ps.DateOffset(days=1),offset=ps.DateOffset(days=1))
		
		values=[Decimal(self.value/len(dates)) for x in dates]
	
		return ps.TimeSeries(values,index=dates)
		
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s-%s, %s, %.2f" % (self.startdate,self.enddate,self.account,self.value) 
		
	@property	
	def actual(self):
		
		actual=self.account.balance_between(self.startdate,self.enddate,True)
		
		return actual
		
		
	@property
	def tomonthly(self):
		
		return self.tofreq('m')
	
	@property
	def toyearly(self):

		return self.tofreq('y')
	
	
	@property
	def toquarterly(self):

		return self.tofreq('q')
	
	@property
	def tosemiannual(self):

		return self.tofreq('s')
		
	
		
		
	
	def tofreq(self,freq):
		
		month_days=30
		
		day_diff=(self.enddate.day-self.startdate.day)+1
		month_diff=(self.enddate.month-self.startdate.month)+1
		year_diff=(self.enddate.year-self.startdate.year)+1
		
		
		if month_diff==1:
			monthly_val=self.value*(month_days/day_diff)
		else:
			monthly_val=self.value/month_diff
		
		if year_diff==1:
			yearly_val = monthly_val*12
		else:
			monthly_val = self.value/(month_diff*year_diff)
			yearly_val = self.value/year_diff
			
		quarterly_val=monthly_val*3
		semi_val=monthly_val*6
			
		if freq=='m':
			return monthly_val
		elif freq=='y':
			return yearly_val
		elif freq=='q':
			return quarterly_val
		elif freq=='s':
			return semi_val
		else:
			return self.value
			
	
		