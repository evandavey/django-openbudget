from django.db import models
from django.contrib.auth.models import Group


class AccountSet(models.Model):

    class Meta: 
        app_label = 'openbudgetapp'

    STYLE_CHOICES = (
        ('P', 'Personal Accounts'),
        ('I', 'Investment Accounts'),
        ('B', 'Business Accounts'),
    )

    name=models.CharField(max_length=255)
    style=models.CharField(max_length=1, choices=STYLE_CHOICES)
    gnucashdb=models.CharField(max_length=255)
    group=models.ForeignKey(Group)

    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return "%s %s" % (self.name,self.style) 
