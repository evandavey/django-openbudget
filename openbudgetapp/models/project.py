from django.db import models

# Create your models here.


class Project(models.Model):

    class Meta: 
        app_label = 'openbudgetapp'


    identifier=models.CharField(max_length=255)

    name=models.CharField(max_length=255)



    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return "%s" % (self.name) 
