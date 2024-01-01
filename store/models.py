from django.db import models
from django.contrib.auth.models import User
from paymentgateway.models import Transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

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

  def __str__(self):
      return self.name

class Becomereseller(models.Model):
  user=models.OneToOneField(User,related_name='becomereseller',on_delete=models.CASCADE)

  def __str__(self):
      return self.user.username
    
class Store(models.Model):
  user=models.OneToOneField(User,related_name='store',on_delete=models.CASCADE)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()

  def __str__(self):
      return self.name

class Wallet(models.Model):
  store=models.ForeignKey(Store,related_name='wallets',on_delete=models.CASCADE)
  currency=models.ForeignKey(Currency,related_name='wallets',on_delete=models.CASCADE)
  balance=models.FloatField(default=0.0)
  
  def __str__(self):
      return f"{self.store.name}#{self.id}: {self.balance} {self.currency.code}"

class Withdraw(models.Model):
  wallet=models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='withdraws')
  amount=models.FloatField()
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

class Order(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
  transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name='orders',null=True)
  draft=models.BooleanField()
  
  def total_cost_number(self):
    amount=0.0
    for sale in self.sales.all():
      amount += sale.sale_price*sale.quantity
    
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
  approved=models.BooleanField(default=False)
  
  def get_sale_price(self):
    return f"{self.sale_price} {self.purchase.currency.code}"
  
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
  
  def get_sale_price(self):
    return f"{self.sale_price} {self.purchase.currency.code}"
  
  def __str__(self):
      return f"{self.purchase.inventory.name} -> Resale {self.sale_price}x{self.quantity}"
  
  