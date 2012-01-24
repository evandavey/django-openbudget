from django.core import management
from django.conf import settings


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
import datetime

#management.call_command('flush', verbosity=0, interactive=False)
#management.call_command('loaddata', 'test_data', verbosity=0)



def gnucash_import(request):
    
    dbfile = getattr(settings, 'GNUCASH_FILE', None)
    
    if dbfile is not None:
        management.call_command('gnucash-import', dbfile,verbosity=1)
        messages.add_message(request, messages.SUCCESS, 'Updated the database from the gnucash file %s' % dbfile)
    else:
        messages.add_message(request, messages.ERROR, 'Please set GNUCASH_FILE in settings.py')
        
    return redirect(request.META.get('HTTP_REFERER','/'))
