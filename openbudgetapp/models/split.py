from django.db import models

# Create your models here.


class Split(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'


	guid=models.CharField(max_length=32,primary_key=True)
	tx=models.ForeignKey("Transaction")
	account=models.ForeignKey("Account")
	value=models.DecimalField(decimal_places=4,max_digits=20)
	
	
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
