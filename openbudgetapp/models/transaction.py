from django.db import models

# Create your models here.


class Transaction(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'


	guid=models.CharField(max_length=32,primary_key=True)
	description=models.CharField(max_length=2048)
	postdate=models.DateField()
	
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s (%s)" % (self.postdate,self.description) 
