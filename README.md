#Open Budget

Simple django-based personal budgeting app that uses GNUCash sqlite data files

#Status

*  basic structure implemented - a gnucash file can be used to import accounts, transactions and splits


#Installation

	$  git clone git://github.com/evandavey/OpenBudget.git openbudget
	$  cd openbudget
 	$  pip install -r requirements/development.txt
	$  fab development syncdb
	$  fab development migratedb


#Usage

##Running the server
	$  fab development runserver

Access the server at: http://127.0.0.0.1:8080/admin/

##Importing a gnucash file

Save your GNUCash file as a sqlite3 file.

	$ ./manage.py gnucash-import <gnucash sql file> --settings=openbudget.settings_local
	

# Dependencies

*  pip:
	$  easy_install pip
	
*  To use the fabfile and fab commands:
	$  pip install fabric
	


