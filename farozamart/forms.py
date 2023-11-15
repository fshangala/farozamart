from django import forms
from farozamart import models

class GeneralOptionsForm(forms.Form):
  name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  tag_line=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

  def save(self):
    models.Option.objects.create(name='name',value=self.cleaned_data['name'])
    models.Option.objects.create(name='tag_line',value=self.cleaned_data['tag_line'])
    models.Option.objects.create(name='description',value=self.cleaned_data['description'])