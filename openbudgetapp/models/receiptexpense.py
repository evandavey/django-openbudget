from django.db import models

# Create your models here.


class ReceiptExpense(models.Model):

    class Meta: 
        app_label = 'openbudgetapp'


    receipt=models.ForeignKey('Receipt')
    value=models.FloatField()
    allocation=models.CharField(max_length=255)
    reimbursable=models.BooleanField(default=False)
    vendor=models.CharField(max_length=255)
    vat=models.FloatField(default=0)
    paidby=models.CharField(max_length=255,default="cash")
	
    def __unicode__(self):
        """ Returns the custom output string for this object
        """
        return "%.2f: %s" % (self.value,self.allocation) 
