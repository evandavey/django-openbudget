from django.db import models
from django.db.models.query import QuerySet
import csv
from django.template.loader import render_to_string

# Create your models here.

class ReceiptQuerySet(QuerySet):



    def data(self):

        data=[]
        headers = ["id","date","transid","client","total","url","note"]
        data.append(headers)
        for r in self:

            if r.tx:
                txid=r.tx.guid
            else:
                txid=None


            data.append([r.id,r.postdate,txid,r.client,r.total,r.url,r.note])

        return data

    def tohtml(self):

        d={}
        d['receipts_list']=self

        return render_to_string('receipts.html',d)

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

class ReceiptManager(models.Manager):


    def get_query_set(self):
        return ReceiptQuerySet(self.model)




class Receipt(models.Model):

    class Meta:
        app_label = 'openbudgetapp'


    postdate=models.DateField()
    note=models.CharField(max_length=2048)
    tx=models.ForeignKey("Transaction",null=True)
    client=models.ForeignKey("Client",null=True)
    url=models.URLField()
    objects=ReceiptManager()

    @property
    def total(self):

        total=0.
        for e in self.receiptexpense_set.all():
            total+=e.value
        return total

    @property
    def reimbursable(self):

        total=0.
        for e in self.receiptexpense_set.filter(reimbursable=True):
            total+=e.value

        return total

    @property
    def expenses(self):

        return self.receiptexpense_set.all()


    def tostring(self):
        s=":::::::: Receipt :::::::::::\n"
        s+="Date:\n\t%s\n" % (self.postdate)
        s+="Client:\n\t%s\n" % (self.client)
        s+="File url:\n\t%s\n" % (self.url)
        s+="Total:\n\t%.2f (%.2f recoverable)\n" % (self.total,self.reimbursable)

        s+="Note:\n\t%s\n" % (self.note)
        s+="Expenses:\n"
        for e in self.receiptexpense_set.all():
            s+="\t%s\n" % (e)

        if self.tx:
            s+="Matched Transaction:\n\t%s id=%s\n" % (self.tx,self.tx.guid)

        if self.tx:
            s+="\tSplits:\n"

            for p in self.tx.splits:
                s+="\t\t%s\n" % (p)
        else:
            s+="Matched Transaction:\n\tNot Found"

        return s


    def __unicode__(self):
        """ Returns the custom output string for this object
        """

        return "%s,%d" % (self.postdate,self.id)
