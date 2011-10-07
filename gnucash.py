import sqlite3
from datetime import *

conn = sqlite3.connect('InvestmentPortfolio.gnucash')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('select a.guid as aID,a.name as aName,a.account_type as aType from accounts as a')
for row in c:
	c2=conn.cursor()
	t = (row['aID'],)
	
	sql = """
	select 
		t.post_date tDate,
		t.description as tDesc,
		s.quantity_num/s.quantity_denom as sValue
	from 
		splits as s 
	left join 
		transactions as t 
	on 
		s.tx_guid=t.guid 
	where 
		s.account_guid=?
	"""
	
	c2.execute(sql, t)
	
	print "%s:%s:%s" % (row['aId'],row['aName'],row['aType'])
	for row2 in c2:
		
		tDate=datetime.strptime(row2['tDate'],"%Y%m%d%H%M%S")
		
		print "...%s:%s,%.2f" % (tDate.strftime('%Y%m%d'),row2['tDesc'],row2['sValue'])
		
		
		
c.close()
