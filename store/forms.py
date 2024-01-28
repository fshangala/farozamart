from django import forms
from store import models
from store import validators
from django.contrib.auth.models import User
from django.core.mail import send_mail
from store import functions
from paymentgateway.models import Transaction
from dropshipping.functions import steadfastCreateOrder, steadfastCreateOrderManual
from dashboard.function import getOptions
from store import signals

class BecomeSellerRequestForm(forms.Form):
  name=forms.CharField(validators=[validators.unique_store_name],widget=forms.TextInput(attrs={'class':'form-control'}),help_text='The name of your store e.g EStore')
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),help_text='Describe your store i.e the products that will be sold on it')
  address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='The physical address of your store e.g EStore')
  email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),help_text='Business email')
  phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Business phone')
  whatsapp=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Business WhatsApp contact',required=False)
  facebook_url=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control'}),help_text='Business facebook URL',required=False)
  trade_licence=forms.ChoiceField(choices=(('Yes','Yes'),('No','No')),widget=forms.Select(attrs={'class':'form-control'}),help_text='Does your business have a trade licence?')
  
  def __init__(self,*args,user:User,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    
    self.initial['address']=self.user.profile.address
    self.initial['email']=self.user.profile.email
    self.initial['phone']=self.user.profile.phone
    self.initial['whatsapp']=self.user.profile.whatsapp
    self.initial['facebook_url']=self.user.profile.facebook_url
  
  def save(self):
    request = models.Becomeseller.objects.create(
      user=self.user,
      name=self.cleaned_data['name'],
      description=self.cleaned_data['description'],
      address=self.cleaned_data['address'],
      email=self.cleaned_data['email'],
      phone=self.cleaned_data['phone'],
      whatsapp=self.cleaned_data['whatsapp'],
      facebook_url=self.cleaned_data['facebook_url'],
      trade_licence=self.cleaned_data['trade_licence']
    )
    
    options = getOptions()
    send_mail(
      f"{options['name']} - Seller request",
      f"Thank you for your request to become a seller at {options['name']}. Your request is under review. We will notify you through this email when it has been accepted or denied.",
      options['site_mail'],
      [self.user.email]
    )
    send_mail(
      f"{options['name']} - Seller request",
      f"{self.user.profile.full_name} has requested to become a seller, please review the request in the dashboard.",
      options['site_mail'],
      [options['site_mail']]
    )

class BecomeSellerForm(forms.Form):
  name=forms.CharField(validators=[validators.unique_store_name],widget=forms.TextInput(attrs={'class':'form-control'}),help_text='The name of your store e.g EStore')
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),help_text='Describe your store i.e the products that will be sold on it')
  address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='The physical address of your store e.g EStore')
  email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),help_text='Business email')
  phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Business phone')
  whatsapp=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Business WhatsApp contact',required=False)
  facebook_url=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control'}),help_text='Business facebook URL',required=False)
  trade_licence=forms.ChoiceField(choices=(('Yes','Yes'),('No','No')),widget=forms.Select(attrs={'class':'form-control'}),help_text='Does your business have a trade licence?')
  
  def __init__(self,*args,user:User,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
  
  def save(self):
    store = models.Store.objects.create(
      user=self.user,
      name=self.cleaned_data['name'],
      description=self.cleaned_data['description'],
      address=self.cleaned_data['address'],
      email=self.cleaned_data['email'],
      phone=self.cleaned_data['phone'],
      whatsapp=self.cleaned_data['whatsapp'],
      facebook_url=self.cleaned_data['facebook_url']
    )
    self.user.profile.is_seller = True
    self.user.save()
    
    options = getOptions()
    send_mail(
      f"{options['name']} - Seller approved",
      f"Your request to become a seller at {options['name']} has been approved. Login with username {self.user.username} and head over to the dashboard.",
      options['site_mail'],
      [self.user.email]
    )
    
class BecomeResellerRequestForm(forms.Form):
  address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='The physical address of your store e.g EStore')
  email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),help_text='Business email')
  phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Business phone')
  whatsapp=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Business WhatsApp contact',required=False)
  facebook_url=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control'}),help_text='Business facebook URL',required=False)

  def __init__(self,*args,user:User,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    
    self.initial['address']=self.user.profile.address
    self.initial['email']=self.user.profile.email
    self.initial['phone']=self.user.profile.phone
    self.initial['whatsapp']=self.user.profile.whatsapp
    self.initial['facebook_url']=self.user.profile.facebook_url
  
  def save(self):
    models.Becomereseller.objects.create(
      user=self.user,
      address=self.cleaned_data['address'],
      email=self.cleaned_data['email'],
      phone=self.cleaned_data['phone'],
      whatsapp=self.cleaned_data['whatsapp'],
      facebook_url=self.cleaned_data['facebook_url']
    )
    
    options = getOptions()
    send_mail(
      f"{options['name']} - Reseller request",
      f"Thank you for your request to become a reseller at {options['name']}. Your request is under review. We will notify you through this email when it has been accepted or denied.",
      options['site_mail'],
      [self.user.email]
    )
    send_mail(
      f"{options['name']} - Reseller request",
      f"{self.user.profile.full_name} has requested to become a reseller, please review the request in the dashboard.",
      options['site_mail'],
      [options['site_mail']]
    )

class BecomeResellerForm(forms.Form):
  address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='The physical address of your store e.g EStore')
  email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),help_text='Business email')
  phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Business phone')
  whatsapp=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Business WhatsApp contact',required=False)
  facebook_url=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control'}),help_text='Business facebook URL',required=False)
  
  def save(self):
    self.user.profile.address=self.cleaned_data['address']
    self.user.profile.email=self.cleaned_data['email']
    self.user.profile.phone=self.cleaned_data['phone']
    self.user.profile.whatsapp=self.cleaned_data['whatsapp']
    self.user.profile.facebook_url=self.cleaned_data['facebook_url']
    self.user.profile.is_reseller = True
    self.user.save()
    
    options = getOptions()
    send_mail(
      f"{options['name']} - Reseller approved",
      f"Your request to become a reseller at {options['name']} has been approved. Login with username {self.user.username} and head over to the dashboard.",
      options['site_mail'],
      [self.user.email]
    )
    
  def __init__(self,*args,user:User,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user

class CategoryForm(forms.Form):
  name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Category name')
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),help_text='Category description')
  
  def save(self):
    if self.instance != None:
      self.instance.name = self.cleaned_data['name']
      self.instance.description = self.cleaned_data['description']
      self.instance.save()
    else:
      models.Category.objects.create(
        user=self.user,
        name=self.cleaned_data['name'],
        description=self.cleaned_data['description']
      )
  
  def __init__(self,*args,user:User,instance:models.Category=None,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.instance=instance
    
    if self.instance:
      self.initial['name']=instance.name
      self.initial['description']=instance.description

class InventoryForm(forms.Form):
  name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Product name')
  description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),help_text='Product description')
  category=forms.ModelChoiceField(queryset=models.Category.objects.none(),widget=forms.Select(attrs={'class':'form-control'}))
  picture=forms.ImageField(help_text='Product featured image')
  
  def save(self):
    if self.instance != None:
      self.instance.name = self.cleaned_data['name']
      self.instance.description = self.cleaned_data['description']
      self.instance.category = self.cleaned_data['category']
      self.instance.picture = self.cleaned_data['picture']
      self.instance.save()
    else:
      inventory = models.Inventory.objects.create(
        store=self.user.store,
        category=self.cleaned_data['category'],
        name=self.cleaned_data['name'],
        description=self.cleaned_data['description'],
        picture=self.cleaned_data['picture']
      )
  
  def __init__(self,*args,user:User,instance:models.Inventory=None,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.instance=instance
    self.fields['category'].queryset=models.Category.objects.all()
    
    if self.instance:
      self.initial['name']=instance.name
      self.initial['description']=instance.description
      self.initial['category']=instance.category
      self.initial['picture']=instance.picture
    else:
      self.fields['name'].validators=[validators.unique_inventory_name]

class InventoryImagesForm(forms.Form):
  picture=forms.ImageField(help_text='Product image')
  
  def __init__(self,*args,inventory:models.Inventory,**kwargs):
    super().__init__(*args,**kwargs)
    self.inventory=inventory
  
  def save(self):
    models.InventoryImage.objects.create(inventory=self.inventory,picture=self.cleaned_data['picture'])
  

class CurrencyForm(forms.Form):
  symbol=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Currency symbol i.e $')
  name_singular=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Currency singular name i.e American Dollar')
  name_plural=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Currency Plural name i.e American dollars')
  code=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Currency 3 character code i.e USD')
  
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
  inventory=forms.ModelChoiceField(queryset=models.Inventory.objects.none(),widget=forms.Select(attrs={'class':'form-control'}),help_text='Choose a product from your inventory.')
  quantity=forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class':'form-control'}), help_text='How much stock you have purchased.')
  purchase_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}), help_text='How much you spent for a single purchase.')
  sale_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}),help_text='How much each purchase will be listed for sale.')
  resale_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}), help_text='How much each purchase will be listed for resale.')
  currency=forms.ModelChoiceField(queryset=models.Currency.objects.all(),widget=forms.Select(attrs={'class':'form-control'}),help_text='Choose a currency for this product.')
  
  def save(self):
    if self.instance:
      self.instance.inventory = self.cleaned_data['inventory']
      self.instance.quantity = self.cleaned_data['quantity']
      self.instance.purchase_price = self.cleaned_data['purchase_price']
      self.instance.sale_price = self.cleaned_data['sale_price']
      self.instance.resale_price = self.cleaned_data['resale_price']
      self.instance.currency = self.cleaned_data['currency']
      self.instance.save()
    else:
      models.Purchase.objects.create(
        inventory=self.cleaned_data['inventory'],
        quantity=self.cleaned_data['quantity'],
        stock=self.cleaned_data['quantity'],
        purchase_price=self.cleaned_data['purchase_price'],
        sale_price=self.cleaned_data['sale_price'],
        resale_price=self.cleaned_data['resale_price'],
        currency=self.cleaned_data['currency']
      )
  
  def __init__(self,*args,user:User,instance:models.Purchase=None,inventory:models.Inventory=None,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.instance=instance
    
    self.fields['inventory'].queryset = user.store.inventory.all()
    
    if inventory:
      self.initial['inventory']=inventory
    
    if self.instance:
      self.initial['inventory']=instance.inventory
      self.initial['quantity']=instance.quantity
      self.initial['purchase_price']=instance.purchase_price
      self.initial['sale_price']=instance.sale_price
      self.initial['resale_price']=instance.resale_price
      self.initial['currency']=instance.currency
    
class SaleForm(forms.Form):
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
      
class AddToResaleCartForm(forms.Form):
  quantity=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))

  def __init__(self,user:User,listing:models.Purchase,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.listing=listing

  def cart(self):
    try:
      order=self.user.orders.get(draft=True,is_reseller=True)
    except Exception as e:
      order=models.Order.objects.create(user=self.user,draft=True,is_reseller=True)
      
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
    

class ResaleForm(forms.Form):
  customer_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  customer_phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  customer_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  quantity=forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class':'form-control'}))
  sale_price=forms.FloatField(min_value=0.0,widget=forms.NumberInput(attrs={'class':'form-control'}))
  
  def save(self):
    order = models.Order.objects.create(
      user=self.reseller,
      draft=False
    )
    models.Resale.objects.create(
      reseller=self.reseller,
      purchase=self.purchase,
      customer_name=self.cleaned_data['customer_name'],
      customer_phone=self.cleaned_data['customer_phone'],
      customer_address=self.cleaned_data['customer_address'],
      quantity=self.cleaned_data['quantity'],
      sale_price=self.cleaned_data['sale_price'],
      order=order
    )
    steadfastCreateOrder(order)
  
  def __init__(self,*args,reseller:User,purchase:models.Purchase,**kwargs):
    super().__init__(*args,**kwargs)
    self.reseller=reseller
    self.purchase=purchase

class ResellerCODCheckout(forms.Form):
  customer_name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  customer_phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  customer_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  
  def __init__(self,*args,reseller:User,order:models.Order,**kwargs):
    super().__init__(*args,**kwargs)
    self.order=order
    self.reseller=reseller
  
  def save(self):
    self.order.customer_name=self.cleaned_data['customer_name']
    self.order.customer_phone=self.cleaned_data['customer_phone']
    self.order.customer_address=self.cleaned_data['customer_address']
    self.order.draft=False
    self.order.save()
    for item in self.order.sales.all():
      item.cart = False
      item.save()
    steadfastCreateOrderManual(self.order,self.cleaned_data['customer_name'],self.cleaned_data['customer_phone'],self.cleaned_data['customer_address'])

class ListingForm(forms.Form):
  quantity=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))

  def __init__(self,user:User,listing:models.Purchase,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.listing=listing

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

class CODCheckoutForm(forms.Form):
  name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  phone=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
  
  def __init__(self,*args,user:User,order:models.Order,**kwargs):
    super().__init__(*args,**kwargs)
    self.user = user
    self.order = order
    
    self.initial['name']=self.user.profile.full_name
    self.initial['phone']=self.user.profile.phone
    self.initial['address']=self.user.profile.address
  
  def save(self):
    self.order.customer_name = self.cleaned_data['name']
    self.order.customer_phone = self.cleaned_data['phone']
    self.order.customer_address = self.cleaned_data['address']

    for item in self.order.sales.all():
      item.cart = False
      item.save()
        
    self.order.draft = False
    self.order.save()
    
    steadfastCreateOrder(self.order)
    signals.order_submitted.send(models.Order,order=self.order)

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
    
    if not self.order.transaction:
      transaction = Transaction.objects.create(
        transaction_id=self.cleaned_data['transaction_id'],
        amount=self.order.total_cost_number()
      )
      self.order.transaction = transaction
    
    self.order.draft = False
    self.order.save()
    
    signals.order_processed.send(sender=models.Order,order=self.order)

class WithdrawRequest(forms.Form):
  amount=forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
  
  def __init__(self,*args,wallet:models.Wallet,**kwargs):
    super().__init__(*args,**kwargs)
    self.wallet=wallet
  
  def save(self):
    withdraw = models.Withdraw.objects.create(
      wallet=self.wallet,
      amount=self.cleaned_data['amount']
    )
    
    signals.withdraw_request_submitted.send(models.Withdraw,withdraw=withdraw)