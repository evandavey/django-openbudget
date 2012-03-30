from openbudgetapp.models import AccountSet
from django import forms

attrs_dict = { 'class': 'required' }


#http://djangosnippets.org/snippets/26/
class AccountSetForm(forms.Form):
    
  

    def __init__(self, qs,*args, **kwargs):
        
        super(AccountSetForm, self).__init__(*args, **kwargs)
        self.fields['accountset'] = forms.ModelChoiceField(queryset=qs)
        
    accountset = forms.ChoiceField(choices=(), widget=forms.Select(attrs=attrs_dict))
    