from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from django.conf import settings
from openbudgetapp.models import Account

urlpatterns = patterns('',

(r'^$','openbudgetapp.views.index'),



)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
