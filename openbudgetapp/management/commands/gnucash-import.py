from django.core.management.base import BaseCommand, CommandError
from openbudgetapp.models import *
import sqlite3
from datetime import *
import os
import sys

	
	
class Command(BaseCommand):
	args = '<gnucash sqllite3 file> <account set id>'
	help = 'Reads a gnucash sqlfile and imports its data into the budget app'

	def handle(self, *args, **options):
			
		if len(args) < 2:
			raise CommandError('Requires arguments %s' % self.args)

		gnucashdb=os.path.join('',args[0])
		accountset=args[1]
		
		try:
		    accset=AccountSet.objects.get(pk=accountset)
		    self.stdout.write(".Using %s\n" % accset.name)
		except:
		    raise CommandError('Could not find account set with id: %d\n%s' % (accountset,sys.exc_info()[1]))	
		

		self.stdout.write('Reading gnucash file %s\n' % (gnucashdb))
		
		try:
			conn = sqlite3.connect(gnucashdb)
		except:
			raise CommandError('db connection failed: %s\n%s' % (gnucashdb,sys.exc_info()[1]))	
		
		conn.row_factory = sqlite3.Row
		
		#self.stdout.write('.Clearing old Accounts\n')
		#Account.objects.all().delete()

		self.stdout.write('.Quering db\n')
		
		c = conn.cursor()
		
		sql="""
		select 
			a.guid as aID,
			a.name as aName,
			a.account_type as aType,
			a.parent_guid as pId,
			a.code as aCode
		
		from accounts as a
		
		"""
		
		c.execute(sql)
		
		self.stdout.write('.Creating accounts\n')
		for r in c:
			
			try:
				a=Account.objects.get(pk=r['aId'],accountset=accset)
			except:
				a=Account()
			
			a.accountset=accset
			a.guid=r['aId']
			a.name=r['aName']
			a.account_type=r['aType']
			a.code=r['aCode']
			#a.parent_id=r['pId']
			a.save()
		
		
		#second loop hack to make sure parents created first
		
		c.execute(sql)

		self.stdout.write('.Adding account parent links\n')
		for r in c:

			try:
				a=Account.objects.get(pk=r['aId'],accountset=accset)
				a.parent_id=r['pId']
				a.save()
			except:
			    pass

			
		
		self.stdout.write('.Clearing old Transactions\n')
		Transaction.objects.filter(accountset=accset).delete()
		sql="""
		select 
			t.guid as tID,
			t.post_date as tPostDate,
			t.num as tNum,
			t.description as tDescription
			
		from transactions as t

		"""

		c.execute(sql)

		self.stdout.write('.Creating transactions\n')
		for r in c:

			t=Transaction()
			t.accountset=accset
			t.guid=r['tId']
			t.description=r['tDescription']
			
			try:
			    t.num=int(r['tNum'])
			except:
			    t.num=None
			
			t.postdate=datetime.strptime(r['tPostDate'],"%Y%m%d%H%M%S")
			
			t.save()


		self.stdout.write('.Clearing old Splits\n')
		Split.objects.filter(accountset=accset).delete()
		sql="""
		select 
			s.guid as sID,
			cast(s.quantity_num as float)/cast(s.quantity_denom as float) as sValue,
			s.tx_guid as tID,
			s.account_guid as aID

		from splits as s 

		"""

		c.execute(sql)

		self.stdout.write('.Creating splits\n')
		for r in c:

			s=Split()
			s.accountset=accset
			s.guid=r['sId']
			s.tx_id=r['tId']
			s.account_id=r['aID']
			s.value=r['sValue']

			s.save()

		
		c.close()
		
		conn.close()