from django.core.management.base import BaseCommand, CommandError
from openbudgetapp.models import *
import sqlite3
from datetime import *

	
	
class Command(BaseCommand):
	args = '<gnucash sqllite3 file>'
	help = 'Reads a gnucash sqlfile and imports its data into the budget app'

	def handle(self, *args, **options):
			
		if len(args) < 1:
			raise CommandError('Requires arguments %s' % self.args)

		gnucashdb=args[0]

		self.stdout.write('Reading gnucash file %s\n' % (gnucashdb))
		
		try:
			conn = sqlite3.connect(gnucashdb)
		except:
			raise CommandError('db connection failed: %s' % gncashdb)	
		
		conn.row_factory = sqlite3.Row
		
		self.stdout.write('.Clearing old Accounts\n')
		Account.objects.all().delete()

		self.stdout.write('.Quering db\n')
		
		c = conn.cursor()
		
		sql="""
		select 
			a.guid as aID,
			a.name as aName,
			a.account_type as aType,
			a.parent_guid as pId
		
		from accounts as a
		
		"""
		
		c.execute(sql)
		
		self.stdout.write('.Creating accounts\n')
		for r in c:
			
			a=Account()
			
			a.guid=r['aId']
			a.name=r['aName']
			a.account_type=r['aType']
			a.parent_id=r['pId']
			a.save()
		
		
			sql="""
			select 
				a.guid as aID,
				a.name as aName,
				a.account_type as aType,
				a.parent_guid as pId

			from accounts as a

			"""

		
		self.stdout.write('.Clearing old Transactions\n')
		Transaction.objects.all().delete()
		sql="""
		select 
			t.guid as tID,
			t.post_date as tPostDate,
			t.description as tDescription
			
		from transactions as t

		"""

		c.execute(sql)

		self.stdout.write('.Creating transactions\n')
		for r in c:

			t=Transaction()

			t.guid=r['tId']
			t.description=r['tDescription']
			
			t.postdate=datetime.strptime(r['tPostDate'],"%Y%m%d%H%M%S")
			
			t.save()


		self.stdout.write('.Clearing old Splits\n')
		Split.objects.all().delete()
		sql="""
		select 
			s.guid as sID,
			s.quantity_num/s.quantity_denom as sValue,
			s.tx_guid as tID,
			s.account_guid as aID

		from splits as s 

		"""

		c.execute(sql)

		self.stdout.write('.Creating splits\n')
		for r in c:

			s=Split()

			s.guid=r['sId']
			s.tx_id=r['tId']
			s.account_id=r['aID']
			s.value=r['sValue']

			s.save()

		
		c.close()
		
		conn.close()