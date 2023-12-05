from django import forms
from dashboard.function import saveOption

class PaylikeConfiguration(forms.Form):
  pass

class CashOnDeliveryConfiguration(forms.Form):
  cod_status=forms.ChoiceField(choices=(('ACTIVATED','Activated'),('DEACTIVATED','Deactivated')), widget=forms.Select(attrs={'class':'form-control'}))
  
  def save(self):
    for x in ['cod_status']:
      saveOption(x,self.cleaned_data[x])