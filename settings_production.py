from openbudget.settings import *

DEBUG = False


GNUCASH_FILE = '/usr/local/web/django/www/production/openbudget/gnucash.db'

STATIC_ROOT = '/usr/local/web/django/www/production/openbudget/static'

TEMPLATE_DIRS = ('/usr/local/web/django/www/production/openbudget/openbudgetapp/templates')


DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'openbudget'             # Or path to database file if using sqlite3.
DATABASE_USER = 'openbudget'             # Not used with sqlite3.
DATABASE_PASSWORD = 'openbudget'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
