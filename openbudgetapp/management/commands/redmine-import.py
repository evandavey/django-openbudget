from django.core.management.base import BaseCommand, CommandError
from openbudgetapp.models import *
import MySQLdb
from datetime import *
import os
import sys
import BeautifulSoup as bs



from StringIO import *

def parseDesc(desc):
    from lxml import etree

    data={}
    dtd = etree.DTD('openbudgetapp/dtds/receipt.dtd')
    try:
        receipt = etree.fromstring(desc)
    except:
        print "Couldn't process - not receipt xml"
        return None


    if not dtd.validate(receipt):
        for e in dtd.error_log.filter_from_errors():
            print e

        return None

    data['date']=receipt.get("date")
    data['id']=receipt.get("id")


    data['url']=receipt.find("url").text

    t=receipt.find("client")
    if t is not None:
        data['clientId']=t.get("id")

    t=receipt.find("project")
    if t is not None:
        data['projectId']=t.get("id")

    n=receipt.find("note")
    data['note']=n.text

    for l in n:
        data['note']+=l.text + l.tail


    expenses=receipt.find("expenses").findall("expense")
    data['expenses']=[]
    for e in expenses:
        edata={'allocation':e.get("allocation"),
               'value':e.text,
               'reimbursable':e.get("reimbursable"),
               'vendor':e.get("vendor"),
               'vat':e.get("paidby"),
               'paidby':e.get("paidby"),

               }

        data['expenses'].append(edata)

    return data

def importClients(conn):
    cursor = conn.cursor()
    cursor = conn.cursor (MySQLdb.cursors.DictCursor)


    sql="""
        SELECT * from contacts

    """

    cursor.execute (sql)

    print 'Saving clients..'
    result_set = cursor.fetchall ()
    for row in result_set:

        try:
            c=Client.objects.get(pk=row['id'])

        except:
            c=Client()

        c.id=row['id']
        c.firstname=row['first_name']
        c.lastname=row['last_name']
        c.company=row['company']

        print "...saving %s" % (str(c))
        c.save()

    cursor.close()


def importProjects(conn):
    sql="""
        SELECT * from projects

    """
    cursor = conn.cursor()
    cursor = conn.cursor (MySQLdb.cursors.DictCursor)

    cursor.execute (sql)

    result_set = cursor.fetchall ()
    for row in result_set:

        try:
            p=Projects.objects.get(identifier=row['identifier'])

        except:
            p=Project()

        p.name=row['name']
        p.identifier=row['identifier']

        p.save()

    cursor.close()

class Command(BaseCommand):
    args = '<account set id>'
    help = 'Imports redmine data into open budget for a given account set'

    def handle(self, *args, **options):

        conn = MySQLdb.connect (host = "macmini.cochranedavey.private",
                                user = "chiliproject",
                                passwd = "cochranedavey1720",
                                db = "chiliproject")



        importClients(conn)
        importProjects(conn)

        if len(args) < 1:
            raise CommandError('Requires arguments %s' % self.args)


        accountset=args[0]
    	try:
		    accset=AccountSet.objects.get(pk=accountset)
		    self.stdout.write(".Using %s\n" % accset.name)
        except:
		    raise CommandError('Could not find account set with id: %d\n%s' % (accountset,sys.exc_info()[1]))




        sql="""
            SELECT id,f.dmsf_file_id,disk_filename,description as 'desc'
            FROM
            (select dmsf_file_id,max(created_at) as latest_date from dmsf_file_revisions group by dmsf_file_id) as x
            JOIN dmsf_file_revisions as f on x.dmsf_file_id=f.dmsf_file_id and x.latest_date=f.created_at
            """
        cursor = conn.cursor()
        cursor = conn.cursor (MySQLdb.cursors.DictCursor)
        cursor.execute (sql)

        Receipt.objects.all().delete()

        result_set = cursor.fetchall ()
        for row in result_set:


            receipt=parseDesc(row['desc'])

            if receipt is not None:


                try:
                    r=Receipt.objects.get(pk=receipt['id'])
                except:
                    r=Receipt()


                try:
                    c=Client.objects.get(pk=receipt['clientId'])
                except:
                    c=None


                r.client=c



                r.id=receipt['id']
                r.postdate=datetime.strptime(receipt['date'],"%Y%m%d").date()
                r.url=receipt['url']

                try:
                    tx=Transaction.objects.get(num=r.id,accountset=accset)
                except:
                    tx=None
                    print sys.exc_info()[1]

                r.tx=tx
                r.note=receipt['note']
                r.save()

                r.receiptexpense_set.all().delete()

                for e in receipt['expenses']:

                    re=ReceiptExpense()
                    re.receipt=r
                    re.value=float(e['value'])
                    re.allocation=e['allocation']
                    re.reimbursable=int(e['reimbursable'])

                    if e['paidby']:
                        re.paidby=e['paidby']
                    else:
                        re.paidby="cash"

                    if e['vat']:
                        re.vat=e['vat']
                    else:
                        re.vat=0.

                    re.vendor=e['vendor']

                    re.save()



            else:
                print 'Invalid markup,skipping'

            # parse the document


        cursor.close ()
        conn.close ()

     