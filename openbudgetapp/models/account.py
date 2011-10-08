from django.db import models
from openbudgetapp.models.split import Split
import numpy as np

class Account(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'


	guid=models.CharField(max_length=32,primary_key=True)
	name=models.CharField(max_length=2048)
	account_type=models.CharField(max_length=2048)
	parent=models.ForeignKey('Account',null=True)
	
	
		
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s (%s)" % (self.name,self.account_type) 
	
			
	
	def splits(self):
		
		qs=Split.objects.filter(account=self)

		if len(qs)==0:
			return None
		vlqs = qs.values_list()
		splits = np.core.records.fromrecords(vlqs, names=[f.name for f in Split._meta.fields])
		
		return splits
	
	@property
	def balance(self):
		
		splits=self.splits()
		
		if splits is None:
			return 0
		
		return splits.value.sum()
		
	
	@property
	def child_balance(self):

		bal=0
		for c in self.child.all()
			bal+=c.balance

		return bal