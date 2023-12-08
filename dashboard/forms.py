from django import forms
from dashboard import models, function

class GeneralOptionsForm(forms.Form):
  name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Enter a unique name for your store or brand.')
  tag_line=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),help_text='Enter a catchy tag-line thats briefly describes your moto')
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),help_text='Describe your store.')
  site_mail=forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={'class':'form-control'}),help_text='Site mail to be contacted on.')
  site_phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Enter store phone number to be contacted on. Usually the help line.')
  business_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Enter business address.')

  def save(self):
    for x in ['name','tag_line','description','site_mail','site_phone','business_address']:
      function.saveOption(x,self.cleaned_data[x])