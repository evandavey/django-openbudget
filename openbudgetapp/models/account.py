from django.db import models

# Create your models here.


class Account(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'


	guid=models.CharField(max_length=32,primary_key=True)
	name=models.CharField(max_length=2048)
	account_type=models.CharField(max_length=2048)
	parent=models.ForeignKey('Account')
	
	