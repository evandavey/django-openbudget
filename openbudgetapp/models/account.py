from django.db import models
from openbudgetapp.models.split import Split
import numpy as np

class Account(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'


	guid=models.CharField(max_length=32,primary_key=True)
	name=models.CharField(max_length=2048)
	account_type=models.CharField(max_length=2048)
	parent=models.ForeignKey('Account',null=True,related_name='child')
	
	
		
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s (%s)" % (self.name,self.account_type) 
	
			
	
	def splits(self,startdate=None,enddate=None):
		
		if startdate is None or enddate is None:
			qs=Split.objects.filter(account=self)
		else:
			qs=Split.objects.filter(account=self,tx__postdate__lte=enddate,tx__postdate__gte=startdate)
			
		if len(qs)==0:
			print "no splits found.."
			return None
			
		vlqs = qs.values_list()
		splits = np.core.records.fromrecords(vlqs, names=[f.name for f in Split._meta.fields])
		
		return splits
	
	
	def balance_between(self,startdate=None,enddate=None,includeChildren=False):
		
	
		splits=self.splits(startdate,enddate)
	
		if splits is None: 
			return 0
			
		bal=splits.value.sum()
		
		if includeChildren:
			for c in self.child.all():
				bal=+c.balance_between(startdate,enddate)
				
		
		return bal
		

	@property
	def balance(self):
		
		splits=self.splits()
		
		if splits is None:
			return 0
		
		return splits.value.sum()
		
	
	@property
	def child_balance(self):

		bal=0
		for c in self.child.all():
			bal+=c.balance

		return bal