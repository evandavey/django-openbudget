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


Access the admin interface at: http://127.0.0.0.1:8080/admin/

##Importing a gnucash file

Save your GNUCash file as a sqlite3 file.

	$ ./manage.py gnucash-import <gnucash sql file> --settings=openbudget.settings_local
	

##Creating budgets

*  Access the admin interface at: http://127.0.0.0.1:8080/admin/ and create or edit AccountBudget objects.

*  Budgets are specified as a total value over a given period.

*  Total amounts will be spread daily over a given analysis period for reporting eg: a yearly budget value will be converted to 365 daily values which will then be multiplied by the number of days in a given month for a monthly report

##The Budget Report

* Access at http://127.0.0.0.1:8080/openbudget/budget/<startdate>/<enddate>/<depth>/<freq>
	
* <startdate> and <enddate> specify the analysis period and should be in YYYYMMDD format

* Depth specifies the depth of the account tree to report on.  

* Freq will define the analysis grouping.  Use 'm' or monthly groups, 'q' for quarterly groups and 'y' for annual groups
	
* For best results, the report should be produced over 6 periods eg: 6 years or 6 quarters or 6 months



# Dependencies

*  pip:

	$  easy_install pip
	
*  To use the fabfile and fab commands:

	$  pip install fabric
	



