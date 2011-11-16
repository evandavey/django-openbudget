"""
This fabfile automates the deployment of github hosted django projects

Author: Evan Davey, evan.j.davey@gmail.com


Instructions:

Modify the environment variables in development,staging or production to
reflect your working environment

To run the project on a development or local machine.

$ fab development bootstrap
$ fab development runserver 

"""

import os,sys

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.decorators import hosts
from contextlib import contextmanager as _contextmanager
from fabric.colors import *


env.project = 'openbudget'
env.git_url = 'git://github.com/evandavey/OpenBudget.git'



def _setup_path():
	env.root = os.path.join(env.home, 'www', env.environment)
	env.code_root = os.path.join(env.root, env.project)
	env.virtualenv_root = os.path.join(env.root, 'env')
	env.settings = '%(project)s.settings_%(environment)s' % env


def development():
	""" Development settings.  Modify these to match your environment """
	env.home = '/Users/evandavey/django-dev/'
	env.environment = 'development'
	env.hosts = ['localhost']
	env.user = 'evandavey'
	env.serverport = '8081'
	_setup_path()

def staging():
	""" use staging environment on remote host"""

	env.home = '/usr/local/web/django'
	env.apacheconfig = '/usr/local/web/config'
	env.user = 'evandavey'
	env.environment = 'staging'
	env.hosts = ['192.168.0.20']
	env.servername = 'openbudget-staging.getoutsideandlive.com'
	_setup_path()


def production():
	env.home = '/usr/local/web/django'
	env.apacheconfig = '/usr/local/web/config'
	
	env.user = 'evandavey'
	env.environment = 'production'
	env.hosts = ['192.168.0.20']
	env.servername = 'openbudget.getoutsideandlive.com'
	_setup_path()


def bootstrap():
	""" sets up host system virtual environment and directory structure """
	
	print(green("Creating project directories"))
	run('mkdir -p %(root)s' % env)
	run('mkdir -p %s' % os.path.join(env.home, 'www', 'log'))
	create_virtualenv()
	clone_remote()
	update_requirements()
	syncdb()
	migratedb()
	collectstatic()
	
def create_virtualenv():
	""" creates a virtual environment """
	
	print(green("Creating a virtual environment in %s" % env.virtualenv_root))
	sudo('WORKON_HOME=%s' % (env.virtualenv_root) + ' && ' + 'source /usr/local/bin/virtualenvwrapper.sh && ' + 'mkvirtualenv --no-site-packages %s' % (env.project),user=env.user)
	

def clone_remote():
	""" Downloads project code from its git repository """
	
	print(green("Cloning repository %s" % env.git_url))
	
	run('rm -rf %s' % os.path.join(env.root,env.project))
	run('git clone %s %s/%s' % (env.git_url,env.root,env.project))


def update_remote():

	pull_remote()
	syncdb()
	migratedb()


def pull_remote():
	
	print(green("Pulling remote repo"))

	with cd(env.code_root):
		run('git pull origin master')
	

def update_requirements():
	""" update external dependencies  """
	
	print(green("Installing dependencies - this may take some time, please be patient"))
	requirements = os.path.join(env.code_root, 'requirements')
	requirements_file=get(os.path.join(requirements, '%s.txt' % env.environment))[0]
	
	with virtualenv():
		## hack to overcome no order in requirements files	
		for line in open(requirements_file, "r"): 
			run("pip install %s" % (line))

	
def syncdb():
	""" syncs the django database """
	
	print(green("Syncing %s database" % env.project))
	
	with virtualenv():
		with cd(env.code_root):
			run('./manage.py syncdb --settings=%s.settings_%s' % (env.project,env.environment))

def migratedb():
	""" syncs the django database """
	
	print(green('Migrating apps in db'))

	with virtualenv():
		with cd(env.code_root):
			run('./manage.py migrate --all --settings=%s.settings_%s' % (env.project,env.environment))


def runserver():
	""" runs the project as a development server """

	require('serverport',provided_by=development)

	print(green('Running development server.  Access at http://127.0.0.1:%s' % env.serverport))

	if env.environment == 'development':
		local('./manage.py runserver 0.0.0.0:%s --settings=%s.settings_%s' % (env.serverport,env.project,env.environment))
		return

	with virtualenv():
		with cd(env.code_root):
			run('./manage.py runserver 0.0.0.0:%s --settings=%s.settings_%s' % (env.serverport,env.project,env.environment))


def collectstatic():
	""" collects static files """

	print(green('Collecting static files'))

	with virtualenv():
		with cd(env.code_root):
			run('./manage.py collectstatic --settings=%s.settings_%s' % (env.project,env.environment))


	
@_contextmanager
def virtualenv():
	""" Wrapper function to ensure code is run under a virtual environment """
	
	venv_dir=os.path.join(env.virtualenv_root, env.project)
	activate='source ' + os.path.join(venv_dir,'bin','activate')

	with prefix(activate):
	    yield
	

def apache_setup():
	
	print(green('Updating apache settings'))
	
	create_apache_conf_files()
	update_apache_conf()
	
def update_apache_conf():
	""" upload apache configuration to remote host """

	require('root', provided_by=('staging', 'production'))

	print(red('moving conf files'))

	conf_dest = os.path.join(env.apacheconfig, 'sites','%(servername)s.conf' % env)
	conf=os.path.join(env.code_root,'install','%s.conf' % env.environment)

	wsgi=os.path.join(env.code_root,'install','%s.wsgi' % env.environment)
	wsgi_dest=os.path.join(env.code_root,'apache','%s.wsgi' % env.environment)

	run('mkdir -p %s' % os.path.join(env.code_root,'apache'))
	run('cp %s %s' % (wsgi,wsgi_dest))
	run('cp %s %s' % (conf,conf_dest))
	apache_reload()


def configtest():    
    """ test Apache configuration """
    require('root', provided_by=('staging', 'production'))
    run('apachectl configtest')


def apache_reload():    
	""" reload Apache on remote host """

	print(red('Reloading apache'))

	require('root', provided_by=('staging', 'production'))
	run('sudo apachectl restart')


def osx_bootstrap():
	""" Performs additional osx bootstrapping """
	
	print(red('Running additional osx bootstrapping'))
	
	create_osx_launchd_file()
	update_osx_launchd_file()

def create_apache_conf_files():
	""" creates apache conf files from templates in ./install/ """

	print(green('Creating apache conf files from templates'))
	
	conf_template=os.path.join(env.code_root,'install','template.conf')
	
	conf_template=get(conf_template)[0]
	
	conf=os.path.join(env.code_root,'install','%s.conf' % env.environment)
	
	wsgi_template=os.path.join(env.code_root,'install','template.wsgi')
	wsgi=os.path.join(env.code_root,'install','%s.wsgi' % env.environment)
	wsgi_template=get(wsgi_template)[0]
	
	r={ 'project':env.project,
		'environment':env.environment,
		'servername':env.servername,
		'home':env.home,
		'certificate-file':os.path.join(env.apacheconfig,'ssl-certificate.conf')
	}
	
	print(red('Replacing %s and saving as %s' % (conf_template,conf)))
	_open_file_and_replace(conf_template,conf_template + ".out",r)
	put(conf_template+ ".out", conf, mode=0755)
	
	print(red('Replacing %s and saving as %s' % (conf_template,conf)))
	_open_file_and_replace(wsgi_template,wsgi_template+".out",r)
	put(wsgi_template+ ".out", wsgi, mode=0755)
	
	
	local('rm -r %s' % env.host)

	
	
	

def create_osx_launchd_file():
	""" creates an osx launchd file from templates in ./install/ """

	print(green('Creating launchd files from templates'))

	conf_template=os.path.join(env.code_root,'install','launchd-template.plist')
	conf_template=get(conf_template)[0]
	
	conf=os.path.join(env.code_root,'install','org.%s-%s.update.plist' % (env.project,env.environment))

	r={ 'project':env.project,
		'environment':env.environment,
		'code_root':env.code_root,
	}

	print(red('Replacing %s and saving as %s' % (conf_template,conf)))
	_open_file_and_replace(conf_template,conf_template + ".out",r)
	put(conf_template+ ".out", conf, mode=0755)
	
def update_osx_launchd_file():
	""" Moves project launchd file to /Library/LaunchDaemons """
	
	launchdf='org.%s-%s.update.plist' % (env.project,env.environment)
	installdir=os.path.join(env.code_root,'install')
	launchddir='/Library/LaunchDaemons/'
	
	src=os.path.join(installdir,launchdf)
	dest=os.path.join(launchddir,launchdf)
	
	with cd(installdir):
		sudo('cp %s %s' % (src,dest))
		sudo('chown root %s' % dest)
		sudo('launchctl load %s' % dest)
		
def remove_osx_launchd_file():
	""" Removes launchd file from /Library/LaunchDaemons """

	launchdf='org.%s-%s.update.plist' % (env.project,env.environment)
	
	launchddir='/Library/LaunchDaemons/'

	dest=os.path.join(launchddir,launchdf)


	sudo('launchctl unload %s' % dest)
	sudo('rm %s' % (dest))
	
		

def _open_file_and_replace(src,dest,replace_dict):
	""" replaces <key> in src with val from key,val of replace_dict with supplied values and saves as dest 
	"""
	
	f=open(src,'r')
	o=open(dest,'w')
	
	for line in f.readlines():
		for k,r in replace_dict.iteritems():
			line=line.replace('<%s>' % k,'%s' % r)
			
		o.write(line+"\n")
		
	f.close()
	o.close()
	
	



