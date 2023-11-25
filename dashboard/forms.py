from django import forms
from dashboard import models, function

class GeneralOptionsForm(forms.Form):
  name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  tag_line=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

  def save(self):
    for x in ['name','tag_line','description']:
      function.saveOption(x,self.cleaned_data[x])