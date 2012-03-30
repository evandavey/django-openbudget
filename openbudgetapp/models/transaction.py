from django.db import models
from django.db.models.query import QuerySet
from django.template.loader import render_to_string


class TransactionQuerySet(QuerySet):
    
    
    
    def data(self):
        
        data=[]
        headers = ["id","date","client","total","receipt-url","receipt-note"]
        data.append(headers)
        for t in self:
            
            try:
                r=t.receipt[0]
            except:
                r=Receipt()
                r.client=None
                r.total=None
                r.note=None
                r.url=None
                r.postdate=None
                
            
              
            data.append([t.id,r.postdate,r.client,r.total,r.url,r.note])
            
        return data
        
    def tohtml(self):
        
        d={}
        d['objlist']=self
        
        return render_to_string('business/transactions.html',d)
    
    def tocsv(self):
        import StringIO
        output=StringIO.StringIO()
        writer = csv.writer(output,quoting=csv.QUOTE_NONNUMERIC)
        
        data=self.data()
        for d in data:
            writer.writerow(d)
        
     
        s=output.getvalue()
        output.close()
        
        return s
        
class TransactionManager(models.Manager):
    
    
    def get_query_set(self):
        return TransactionQuerySet(self.model)
   
    



class Transaction(models.Model):

	class Meta: 
		app_label = 'openbudgetapp'
		
	accountset=models.ForeignKey("AccountSet")

	guid=models.CharField(max_length=32,primary_key=True)
	description=models.CharField(max_length=2048)
	postdate=models.DateField()
	num=models.IntegerField(null=True,blank=True)
	
	objects = TransactionManager()
	
	@property
	def receipt_missing(self):
	    
	    receipt_missing=True
	    
	    receipt_required=False
	    for s in self.splits:
	        if s.account.account_type=='EXPENSE':
	            receipt_required=True
	            break
	    
	    
	    
	    if receipt_required==False or self.receipt:
	        return False
	    else:
	        return True
	
	@property
	def receipt(self):
	    
	    r=self.receipt_set.all()
	
	    try:
	        return r[0]
	    except:
	        return None
	
	@property
	def total(self):
	    
	    total=0.
	    
	    for s in self.splits:
	        total+=abs(float(s.value))/2
	        
	    return total
	    
	@property
	def splits(self):
	    
	    return self.split_set.all()
	
	def __unicode__(self):
		""" Returns the custom output string for this object
		"""
		s="%s %.2f (%s)" % (self.postdate,float(self.total),self.description)
	
		
		return s
