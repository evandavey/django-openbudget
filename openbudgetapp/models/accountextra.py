from django.db import models


class AccountExtra(models.Model):
    
    
    class Meta: 
        
        app_label = 'openbudgetapp'
        
    account=models.ForeignKey('Account')
    pct_discrentionary=models.DecimalField(decimal_places=4,max_digits=20,default=0)
    inflation_category=models.CharField(max_length=255,default='NONE')
    investment_category=models.CharField(max_length=255,default='NONE')
    asset_class=models.CharField(max_length=255,default='NONE')
    
    
    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        
        return "%s (%s)" % (self.account.formatted_name,self.account.account_type)
	