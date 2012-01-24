from django.db import models


class InflationRate(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'
		ordering = ['enddate']
		
		
	category=models.CharField(max_length=255)
	startdate=models.DateField()
	enddate=models.DateField()
	rate=models.DecimalField(decimal_places=4,max_digits=20)
	
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		return "%s - %s - %.2f" % (self.category,self.enddate,self.rate*100)
		
		
	