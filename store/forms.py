from django import forms
from store import models
from store import validators
from django.contrib.auth.models import User
from store import functions

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
  user=None
  instance=None
  name=forms.CharField(validators=[validators.unique_inventory_name],widget=forms.TextInput(attrs={'class':'form-control'}))
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
  
  def save(self):
    if self.instance != None:
      self.instance.name = self.cleaned_data['name']
      self.instance.description = self.cleaned_data['description']
      self.instance.save()
    else:
      inventory = models.Inventory.objects.create(store=self.user.store,name=self.cleaned_data['name'],description=self.cleaned_data['description'])
  
  def __init__(self,*args,user:User,instance:models.Inventory=None,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.instance=instance
    
    if self.instance:
      self.initial['name']=instance.name
      self.initial['description']=instance.description

class PurchaseForm(forms.Form):
  user=None
  instance=None
  inventory=forms.ModelChoiceField(queryset=models.Inventory.objects.none(),widget=forms.Select(attrs={'class':'form-control'}))
  quantity=forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class':'form-control'}))
  purchase_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}))
  sale_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}))
  
  def save(self):
    if self.instance:
      self.instance.inventory = self.cleaned_data['inventory']
      self.instance.quantity = self.cleaned_data['quantity']
      self.instance.purchase_price = self.cleaned_data['purchase_price']
      self.instance.sale_price = self.cleaned_data['sale_price']
      self.instance.save()
    else:
      models.Purchase.objects.create(
        inventory=self.cleaned_data['inventory'],
        quantity=self.cleaned_data['quantity'],
        purchase_price=self.cleaned_data['purchase_price'],
        sale_price=self.cleaned_data['sale_price'],
      )
  
  def __init__(self,*args,user:User,instance:models.Purchase=None,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.instance=instance
    
    self.fields['inventory'].queryset = user.store.inventory.all()
    
    if self.instance:
      self.initial['inventory']=instance.inventory
      self.initial['quantity']=instance.quantity
      self.initial['purchase_price']=instance.purchase_price
      self.initial['sale_price']=instance.sale_price
    
class SaleForm(forms.Form):
  user=None
  instance=None
  purchase=forms.ModelChoiceField(queryset=models.Purchase.objects.none(),widget=forms.Select(attrs={'class':'form-control'}))
  quantity=forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class':'form-control'}))
  sale_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}))
  
  def save(self):
    if self.instance:
      self.instance.purchase = self.cleaned_data['purchase']
      self.instance.quantity = self.cleaned_data['quantity']
      self.instance.sale_price = self.cleaned_data['sale_price']
      self.instance.save()
    else:
      models.Sale.objects.create(
        purchase=self.cleaned_data['purchase'],
        quantity=self.cleaned_data['quantity'],
        sale_price=self.cleaned_data['sale_price'],
      )
  
  def __init__(self,*args,user:User,instance:models.Sale=None,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.instance=instance
    
    self.fields['purchase'].queryset = functions.getUserPurchases(user)
    
    if self.instance:
      self.initial['purchase']=instance.purchase
      self.initial['quantity']=instance.quantity
      self.initial['sale_price']=instance.sale_price

class ListingForm(forms.Form):
  quantity=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))

  def buy(self):
    pass

  def cart(self):
    pass
    