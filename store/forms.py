from django import forms
from store import models
from store import validators
from django.contrib.auth.models import User
from store import functions
from paymentgateway.models import Transaction
from dropshipping.functions import steadfastCreateOrder

class BecomeSellerForm(forms.Form):
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
  name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
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
    else:
      self.fields['name'].validators=[validators.unique_inventory_name]

class CurrencyForm(forms.Form):
  symbol=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control'}))
  name_singular=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  name_plural=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  code=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control'}))
  
  def save(self):
    if self.instance != None:
      self.instance.symbol=self.cleaned_data['symbol']
      self.instance.name_singular=self.cleaned_data['name_singular']
      self.instance.name_plural=self.cleaned_data['name_plural']
      self.instance.code=self.cleaned_data['code']
      self.instance.save()
    else:
      models.Currency.objects.create(
        symbol=self.cleaned_data['symbol'],
        name_singular=self.cleaned_data['name_singular'],
        name_plural=self.cleaned_data['name_plural'],
        code=self.cleaned_data['code']
      )
  
  def __init__(self,*args,instance:models.Currency=None,**kwargs):
    super().__init__(*args,**kwargs)
    self.instance=instance
    
    if self.instance:
      self.initial.update({
        'symbol':instance.symbol,
        'name_singular':instance.name_singular,
        'name_plural':instance.name_plural,
        'code':instance.code
      })
    else:
      self.fields['symbol'].validators=[validators.CurrencyValidators.unique_symbo]
      self.fields['code'].validators=[validators.CurrencyValidators.unique_code]

class PurchaseForm(forms.Form):
  user=None
  instance=None
  inventory=forms.ModelChoiceField(queryset=models.Inventory.objects.none(),widget=forms.Select(attrs={'class':'form-control'}))
  quantity=forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class':'form-control'}))
  purchase_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}))
  sale_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}))
  currency=forms.ModelChoiceField(queryset=models.Currency.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
  
  def save(self):
    if self.instance:
      self.instance.inventory = self.cleaned_data['inventory']
      self.instance.quantity = self.cleaned_data['quantity']
      self.instance.purchase_price = self.cleaned_data['purchase_price']
      self.instance.sale_price = self.cleaned_data['sale_price']
      self.instance.currency = self.cleaned_data['currency']
      self.instance.save()
    else:
      models.Purchase.objects.create(
        inventory=self.cleaned_data['inventory'],
        quantity=self.cleaned_data['quantity'],
        purchase_price=self.cleaned_data['purchase_price'],
        sale_price=self.cleaned_data['sale_price'],
        currency=self.cleaned_data['currency']
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
      self.initial['currency']=instance.currency
    
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

  def __init__(self,user:User,listing:models.Purchase,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.listing=listing

  def buy(self):
    pass

  def cart(self):
    try:
      order=self.user.orders.get(draft=True)
    except Exception as e:
      order=models.Order.objects.create(user=self.user,draft=True)
      
    current = models.Sale.objects.filter(user=self.user,purchase=self.listing,cart=True).first()
    if current:
      current.quantity += self.cleaned_data['quantity']
      current.save()
    else:
      sale = models.Sale.objects.create(
        user=self.user,
        purchase=self.listing,
        quantity=self.cleaned_data['quantity'],
        sale_price=self.listing.sale_price,
        order=order,
        cart=True,
        approved=False
      )

class CheckoutForm(forms.Form):
  transaction_id=forms.CharField(max_length=200)
  amount=forms.FloatField()
  
  def __init__(self,*args,order_id,**kwargs):
    super().__init__(*args,**kwargs)
    self.order_id=order_id
  
  def save(self):
    order = models.Order.objects.get(pk=self.order_id)
    for item in order.sales.all():
      item.cart = False
      item.save()
      wallet = item.purchase.inventory.store.wallets.filter(currency=item.purchase.currency).first()
      if wallet:
        wallet.balance += item.sale_price*item.quantity
        wallet.save()
      else:
        wallet = models.Wallet.objects.create(store=item.purchase.inventory.store,currency=item.purchase.currency)
        wallet.balance += item.sale_price*item.quantity
        wallet.save()
        
    transaction = Transaction.objects.create(
      transaction_id=self.cleaned_data['transaction_id'],
      amount=self.cleaned_data['amount']
    )
    order.draft = False
    order.transaction = transaction
    order.save()
    steadfastCreateOrder(order)

class ApproveOrderForm(forms.Form):
  transaction_id=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control','read-only':True}))
  amount=forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','readonly':True}))
  
  def __init__(self,*args,order:models.Order,**kwargs):
    super().__init__(*args,**kwargs)
    self.order=order
  
  def save(self):
    for item in self.order.sales.all():
      item.approve()
        
    transaction = Transaction.objects.create(
      transaction_id=self.cleaned_data['transaction_id'],
      amount=self.order.total_cost_number()
    )
    
    self.order.draft = False
    self.order.transaction = transaction
    self.order.save()
    
    steadfastCreateOrder(self.order)

class WithdrawRequest(forms.Form):
  amount=forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
  
  def __init__(self,*args,wallet:models.Wallet,**kwargs):
    super().__init__(*args,**kwargs)
    self.wallet=wallet
  
  def save(self):
    models.Withdraw.objects.create(
      wallet=self.wallet,
      amount=self.cleaned_data['amount']
    )