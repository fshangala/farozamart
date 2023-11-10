from django import forms
from store import models
from store import validators
from django.contrib.auth.models import User

class BecomeSellerForm(forms.Form):
  user=None
  name=forms.CharField(validators=[validators.unique_store_name],widget=forms.TextInput(attrs={'class':'form-control'}),help_text='The name of your store e.g EStore')
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),help_text='Describe your store i.e the products that will be sold on it')
  
  def __init__(self,*args,user:User,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
  
  def save(self):
    store = models.Store.objects.create(user=self.user,name=self.cleaned_data['name'],description=self.cleaned_data['description'])
    self.user.profile.is_seller = True
    self.user.save()

class InventoryForm(forms.Form):
  store=forms.ModelChoiceField(models.Store.objects.all())
  name=forms.CharField(validators=[validators.unique_inventory_name],widget=forms.Textarea(attrs={'class':'form-control'}))
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
  
  def save(self):
    inventory = models.Inventory.objects.create(store=self.cleaned_data['store'],name=self.cleaned_data['name'],description=self.cleaned_data['description'])
  
  def __init__(self,*args,user:User,**kwargs):
    super().__init__(*args,**kwargs)
    self.store=forms.ModelChoiceField(models.Store.objects.filter(user=user),widget=forms.Select(attrs={'class':'form-control'}))