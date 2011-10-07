from django.db import models

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
		return "%s (%s)" % (self.postdate,self.description) 
