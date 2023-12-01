from django import forms
from dashboard.function import saveOption

class SteadfastConfiguration(forms.Form):
  steadfast_api_key=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  steadfast_api_secrete=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  
  def save(self):
    for x in ['steadfast_api_key','steadfast_api_secrete']:
      saveOption(x,self.cleaned_data[x])