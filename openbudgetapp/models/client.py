from django.db import models

# Create your models here.


class Client(models.Model):

    class Meta: 
        app_label = 'openbudgetapp'


    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    company=models.CharField(max_length=255)



    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return "%s %s (%s)" % (self.firstname,self.lastname,self.company) 
