from django.db import models
from django.contrib.auth.models import User
from paymentgateway.models import Transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from dashboard.function import getOptions

# Create your models here.
    
class Currency(models.Model):
  symbol=models.CharField(max_length=10,unique=True)
  name_singular=models.CharField(max_length=200)
  name_plural=models.CharField(max_length=200)
  code=models.CharField(max_length=10,unique=True)
  
  def __str__(self):
      return self.name_singular

class Becomeseller(models.Model):
  user=models.OneToOneField(User,related_name='becomeseller',on_delete=models.CASCADE)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()
  address=models.CharField(max_length=200)
  email=models.EmailField()
  phone=models.CharField(max_length=200)
  whatsapp=models.CharField(max_length=200,null=True)
  facebook_url=models.URLField(null=True)
  trade_licence=models.CharField(max_length=200,choices=(('Yes','Yes'),('No','No')),default='No')

  def __str__(self):
      return self.name

class Becomereseller(models.Model):
  user=models.OneToOneField(User,related_name='becomereseller',on_delete=models.CASCADE)
  address=models.CharField(max_length=200)
  email=models.EmailField()
  phone=models.CharField(max_length=200)
  whatsapp=models.CharField(max_length=200,null=True)
  facebook_url=models.URLField(null=True)

  def __str__(self):
      return self.user.username
    
class Store(models.Model):
  user=models.OneToOneField(User,related_name='store',on_delete=models.CASCADE)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()
  address=models.CharField(max_length=200)
  email=models.EmailField()
  email_verified=models.BooleanField(default=False)
  phone=models.CharField(max_length=200)
  whatsapp=models.CharField(max_length=200,null=True)
  facebook_url=models.URLField(null=True)

  def __str__(self):
      return self.name

class Wallet(models.Model):
  store=models.ForeignKey(Store,related_name='wallets',on_delete=models.CASCADE)
  currency=models.ForeignKey(Currency,related_name='wallets',on_delete=models.CASCADE)
  balance=models.FloatField(default=0.0)
  
  def __str__(self):
      return f"{self.store.name}#{self.id}: {self.balance} {self.currency.code}"

class StoreWallet(models.Model):
  store=models.ForeignKey(Store,related_name='store_wallets',on_delete=models.CASCADE)
  currency=models.ForeignKey(Currency,related_name='store_wallets',on_delete=models.CASCADE)
  balance_before=models.FloatField(default=0.0)
  balance_after=models.FloatField(default=0.0)
  transaction_reference=models.CharField(max_length=200)
  timestamp=models.DateTimeField(default=timezone.now())
  
  def __str__(self):
      return f"{self.store.name}#{self.id}: {self.balance_after} {self.currency.code}"

class UserWallet(models.Model):
  user=models.OneToOneField(User,related_name='user_wallets',on_delete=models.CASCADE)
  currency=models.ForeignKey(Currency,related_name='user_wallets',on_delete=models.CASCADE)
  balance_before=models.FloatField(default=0.0)
  balance_after=models.FloatField(default=0.0)
  transaction_reference=models.CharField(max_length=200)
  timestamp=models.DateTimeField(default=timezone.now())
  
  def __str__(self):
      return f"{self.user.username}#{self.id}: {self.balance_after} {self.currency.code}"

class Withdraw(models.Model):
  wallet=models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='withdraws')
  amount=models.FloatField()
  bkash_number=models.CharField(max_length=200,null=True)
  nid_card=models.ImageField(upload_to='kyc/',null=True)
  transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name='withdraws',null=True)
  approved=models.BooleanField(default=False)
  
  def __str__(self):
      return f"Withdraw {self.amount}"  

class Category(models.Model):
  user=models.ForeignKey(User,related_name='categories',on_delete=models.CASCADE)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()
  
  def __str__(self):
      return self.name

class Inventory(models.Model):
  store=models.ForeignKey(Store,related_name='inventory',on_delete=models.CASCADE)
  category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='inventory',null=True)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()
  picture=models.ImageField(upload_to='products',default='products/default.png')

  def __str__(self):
      return self.name

class InventoryImage(models.Model):
  inventory=models.ForeignKey(Inventory,related_name='images',on_delete=models.CASCADE)
  picture=models.ImageField(upload_to='products/detail')
  
  def __str__(self):
      return self.picture.name

class Purchase(models.Model):
  inventory=models.ForeignKey(Inventory,related_name='purchases',on_delete=models.CASCADE)
  quantity=models.IntegerField()
  stock=models.IntegerField()
  purchase_price=models.FloatField()
  sale_price=models.FloatField()
  resale_price=models.FloatField(default=0.0)
  sku=models.CharField(max_length=100,unique=True,null=True)
  currency=models.ForeignKey(Currency,related_name='purchases',on_delete=models.CASCADE)
  
  def generateSKU(self)->str:
    return f"F{self.inventory.store.id}{self.inventory.id}{self.inventory.category.id}{self.id}"
  
  def get_purchase_price(self):
    return f"{self.purchase_price} {self.currency.code}"
  
  def get_sale_price(self):
    return f"{self.sale_price} {self.currency.code}"
  
  def get_resale_price(self):
    value=""
    if self.resale_price > 0:
      value = f"{self.resale_price} {self.currency.code}"
    return value

  def __str__(self):
      return f"{self.inventory.name} -> Purchase {self.purchase_price}x{self.quantity}"
  
@receiver(post_save, sender=Purchase)
def _post_save_receiver(sender, instance, created, **kwargs):
  if not instance.sku:
    instance.sku = instance.generateSKU()
    instance.save()

order_status=(
  ('DRAFT','Draft'),
  ('PENDING','Pending'),
  ('COMFIRMED','Comfirmed'),
  ('COMPLETE','Complete'),
  ('DECLINED','Declined'),
)
class Order(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
  customer_name=models.CharField(max_length=200,null=True)
  customer_phone=models.CharField(max_length=200,null=True)
  customer_address=models.CharField(max_length=200,null=True)
  transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name='orders',null=True)
  delivery_area=models.CharField(max_length=200,null=True)
  is_reseller=models.BooleanField(default=False)
  own_delivery_charge=models.FloatField(default=0)
  advance_payment=models.FloatField(default=0)
  draft=models.BooleanField(default=False)
  status=models.CharField(max_length=200,default='DRAFT')
  created_at=models.DateTimeField(default=timezone.now())
  updated_at=models.DateTimeField(default=timezone.now())
  
  def delivery_fee(self):
    fee = 0.0
    if self.delivery_area:
      options=getOptions()
      if self.delivery_area == 'OUTSIDE_DHAKA':
        fee = float(options['steadfast_delivery_outside_dhaka'])
      elif self.delivery_area == 'INSIDE_DHAKA':
        fee = float(options['steadfast_delivery_inside_dhaka'])
    
    return fee
  
  def reseller_profit_percentage(self):
    return (self.total_reseller_profit() / self.total_cost_number())*100
  
  def total_reseller_profit(self):
    total=0.0
    if self.sales.all():
      for sale in self.sales.all():
        total+=sale.reseller_profit()
    return total
  
  def total_cost_number(self):
    amount=0.0
    for sale in self.sales.all():
      amount += sale.cost()
    
    amount += self.delivery_fee()
    
    return amount
  
  def total_cost(self):
    amount=0.0
    currency=None
    sales = self.sales.all()
    resales = self.resales.all()
    
    if sales.count() > 0:
      for sale in sales:
        amount += sale.sale_price*sale.quantity
        currency = sale.purchase.currency
    
    elif resales.count() > 0:
      for resale in resales:
        amount += resale.sale_price*resale.quantity
        currency = resale.purchase.currency
    
    return f"{amount} {currency.code}"
  
  def __str__(self):
    return f"{self.user.username};#{self.id};{self.sales.count()}"

class Sale(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sales')
  purchase=models.ForeignKey(Purchase,related_name='sales',on_delete=models.CASCADE)
  quantity=models.IntegerField()
  sale_price=models.FloatField()
  order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='sales')
  cart=models.BooleanField(default=True)
  resale=models.BooleanField(default=False)
  approved=models.BooleanField(default=False)
  
  def purchase_cost(self)->float:
    """Cost according to sale quantity and purchase price"""
    return self.quantity*self.purchase.purchase_price
  
  def cost(self)->float:
    """Total cost according to sale quantity and sale price"""
    return self.quantity*self.sale_price
  
  def seller_cost(self)->float:
    """Cost according to sale quantity and resale price"""
    return self.quantity*self.purchase.resale_price
  
  def reseller_cost(self)->float:
    """Cost that the reseller adds for a resale"""
    return self.cost() - self.seller_cost()
  
  def profit(self)->float:
    """Total profit on the sale"""
    return self.cost() - self.purchase_cost()
  
  def seller_profit(self):
    """Profit for the seller in a resale"""
    return self.seller_cost() - self.purchase_cost()
  
  def reseller_profit(self):
    """Profit for the reseller in a resale"""
    return self.profit() - self.seller_profit()
  
  def approve(self):
    self.purchase.stock -= self.quantity
    self.purchase.save()
    
    self.cart = False
    self.approved = True
    self.save()
  
    wallet = self.purchase.inventory.store.wallets.filter(currency=self.purchase.currency).first()
    if wallet:
      wallet.balance += self.sale_price*self.quantity
      wallet.save()
    else:
      wallet = Wallet.objects.create(store=self.purchase.inventory.store,currency=self.purchase.currency)
      wallet.balance += self.sale_price*self.quantity
      wallet.save()
  
  def sale(self):
    storeWallet=self.purchase.inventory.store.store_wallets.filter(currency=self.purchase.currency).first()
    storeAfter=storeWallet.balance_after if storeWallet != None else 0.0
    if self.resale:
      userWallet=self.order.user.user_wallets.filter(currency=self.purchase.currency).first()
      userAfter=userWallet.balance_after if userWallet != None else 0.0
      
      StoreWallet.objects.create(
        store=self.purchase.inventory.store,
        currency=self.purchase.currency,
        balance_before=storeAfter,
        balance_after=storeAfter+self.seller_cost(),
        transaction_reference=f"Resold listing {self.purchase.id} from order {self.order.id}"
      )
      UserWallet.objects.create(
        store=self.purchase.inventory.store,
        currency=self.purchase.currency,
        balance_before=userAfter,
        balance_after=userAfter+self.reseller_cost(),
        transaction_reference=f"Resold listing {self.purchase.id} from order {self.order.id}"
      )
    else:
      StoreWallet.objects.create(
        store=self.purchase.inventory.store,
        currency=self.purchase.currency,
        balance_before=storeAfter,
        balance_after=storeAfter+self.cost(),
        transaction_reference=f"Sold listing {self.purchase.id} from order {self.order.id}"
      )
      
    self.purchase.stock -= self.quantity
    self.purchase.save()
    
    self.approve=True
    self.save()

  def __str__(self):
      return f"{self.purchase.inventory.name} -> Sale {self.sale_price}x{self.quantity}"

class Resale(models.Model):
  reseller=models.ForeignKey(User,on_delete=models.CASCADE,related_name='resales')
  customer_name=models.CharField(max_length=200)
  customer_phone=models.CharField(max_length=200)
  customer_address=models.CharField(max_length=200)
  purchase=models.ForeignKey(Purchase,related_name='resales',on_delete=models.CASCADE)
  quantity=models.IntegerField()
  sale_price=models.FloatField()
  order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='resales')
  approved=models.BooleanField(default=False)
  
  def profit(self)->float:
    return (self.sale_price*self.quantity) - (self.purchase.purchase_price*self.quantity)
  
  def seller_profit(self):
    return (self.purchase.resale_price*self.quantity) - (self.purchase.purchase_price*self.quantity)
  
  def reseller_profit(self):
    return self.profit() - self.seller_profit()
  
  def get_sale_price(self):
    return f"{self.sale_price} {self.purchase.currency.code}"
  
  def __str__(self):
      return f"{self.purchase.inventory.name} -> Resale {self.sale_price}x{self.quantity}"
  
  