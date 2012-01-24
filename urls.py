from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

(r'^$',include('openbudgetapp.urls')),

(r'^openbudgetapp/', include('openbudgetapp.urls')),

(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

(r'^admin/', include(admin.site.urls)),

)





