from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from openbudgetapp.models import AccountSet,Transaction

@login_required(login_url='/accounts/login')
def transaction_journal(request,accountset_id):
    accountset=AccountSet.objects.get(pk=accountset_id)

    objlist=Transaction.objects.filter(accountset=accountset)

    ct={'objlist':objlist,

    }

    return render_to_response('openbudgetapp/business/transactions.html',ct,context_instance=RequestContext(request))