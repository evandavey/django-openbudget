from django.db import models
from openbudgetapp.models.split import Split
# Create your models here.


class AccountBudget(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'


	account=models.ForeignKey("Account")
	value=models.DecimalField(decimal_places=4,max_digits=20)
	startdate=models.DateField()
	enddate=models.DateField()
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s-%s, %s, %.2f" % (self.startdate,self.enddate,self.account,self.value) 
		
	@property	
	def actual(self):
		
		actual=self.account.balance_between(self.startdate,self.enddate,True)
		
		return actual
		
		

		