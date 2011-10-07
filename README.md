[GNUCash]: http://www.gnucash.org

#Open Budget

Simple django-based personal budgeting app that uses [GNUCash][] sqlite data files.

#Motivation
This project serves two main purposes:

1. get data out of gnucash and into the django framework to allow for more flexible analysis eg: using the numpy maths library

2. implement basic budget functionality to allow a flexible budgeted vs actual report

GNUCash works as a good tool for data entry and standard accounting reports like balance sheets and profit & loss. However, report customisation is overly complicated and the budget functionality poor.  This project aims to address these issues.


#Status

*  basic structure implemented - a gnucash file can be used to import accounts, transactions and splits


#Installation

	$  git clone git://github.com/evandavey/OpenBudget.git openbudget
	$  cd openbudget
 	$  pip install -r requirements/development.txt

If fabric is installed:

	$  fab development syncdb
	$  fab development migratedb

Otherwise:

	$  ./manage.py syncdb --settings=openbudget.settings_local
	$  ./manage.py schemamigration openbudgetapp --settings=openbudget.settings_local


#Usage

##Running the server

If fabric is installed:

	$  fab development runserver
	
Otherwise:

	$  ./manage.py runserver 0.0.0.0:8080 --settings=openbudget.settings_local


Access the server at: http://127.0.0.0.1:8080/admin/

##Importing a gnucash file

Save your GNUCash file as a sqlite3 file.

	$ ./manage.py gnucash-import <gnucash sql file> --settings=openbudget.settings_local
	

# Dependencies

*  pip:

	$  easy_install pip
	
*  To use the fabfile and fab commands:

	$  pip install fabric
	



