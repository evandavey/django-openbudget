from django.core import management
from django.conf import settings


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
import datetime
from openbudgetapp.models import AccountSet
#management.call_command('flush', verbosity=0, interactive=False)
#management.call_command('loaddata', 'test_data', verbosity=0)


@login_required(login_url='/accounts/login')
def gnucash_import(request,accountset_id):
    
    accountset=AccountSet.objects.get(pk=accountset_id)
    dbfile = accountset.gnucashdb
    
    if dbfile is not None:
        management.call_command('gnucash-import', dbfile,accountset_id,verbosity=1)
        messages.add_message(request, messages.SUCCESS, 'Updated the database from the gnucash file %s' % dbfile)
    else:
        messages.add_message(request, messages.ERROR, 'Please set GNUCASH_FILE in settings.py')
        
    return redirect(request.META.get('HTTP_REFERER','/'))


@login_required(login_url='/accounts/login')
def redmine_import(request,accountset_id):

    accountset=AccountSet.objects.get(pk=accountset_id)

    
    management.call_command('redmine-import', accountset_id,verbosity=1)
    messages.add_message(request, messages.SUCCESS, 'Updated the database from redmine for %s' % accountset.name)
    
    return redirect(request.META.get('HTTP_REFERER','/'))