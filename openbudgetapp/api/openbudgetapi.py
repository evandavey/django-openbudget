from tastypie.resources import ModelResource
from tastypie import fields

from openbudgetapp.models import Transaction,AccountSet
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
from tastypie.constants import ALL, ALL_WITH_RELATIONS


models.signals.post_save.connect(create_api_key, sender=User)

class CustomApiKeyAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        username =  request.META.get('HTTP_X_USERNAME')   or request.GET.get('username')
        api_key =   request.META.get('HTTP_X_APIKEY')     or request.GET.get('apikey')

        if not username or not api_key:
            return self._unauthorized()
        try:
            user = User.objects.get(username=username)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return self._unauthorized()
        request.user = user
        return self.get_key(user, api_key)

class AccountSetResource(ModelResource):
    
    class Meta:
        queryset = AccountSet.objects.all()
        resource_name = 'accountset'
        allowed_methods = ['get']
        #authentication = CustomApiKeyAuthentication()
        #authorization = DjangoAuthorization()

class TransactionResource(ModelResource):
    
    accountset = fields.ForeignKey(AccountSetResource, 'accountset',full=True)
    
    class Meta:
        queryset = Transaction.objects.all()
        resource_name = 'transaction'
        allowed_methods = ['get']
        #authentication = CustomApiKeyAuthentication()
        #authorization = DjangoAuthorization()
        
        filtering = {
                    "accountset": ('exact',),
        }
        
    def alter_list_data_to_serialize(self, request, data):
        data['locations'] = data['objects']
        del data['objects']
        return data

    def alter_deserialized_list_data(self, request, data):
        data['objects'] = data['locations']
        del data['locations']
        return data


     
    #filter to only user records...   
    #def apply_authorization_limits(self, request, object_list):
    #    return object_list.filter(user=request.user.name)