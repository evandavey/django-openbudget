from django.db import models
from openbudgetapp.models.split import Split
from openbudgetapp.models.accountbudget import AccountBudget

import numpy as np
from decimal import *

class Account(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'


	guid=models.CharField(max_length=32,primary_key=True)
	name=models.CharField(max_length=2048)
	account_type=models.CharField(max_length=2048)
	parent=models.ForeignKey('self',null=True,related_name='child')
	
	@property
	def formatted_name(self):
		
		names=[]
		parent=self.parent
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
		return "%s (%s)" % (self.name,self.account_type) 
	
			
	
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
	