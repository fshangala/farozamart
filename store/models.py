from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Currency(models.Model):
  symbol=models.CharField(max_length=10,unique=True)
  name_singular=models.CharField(max_length=200)
  name_plural=models.CharField(max_length=200)
  code=models.CharField(max_length=10,unique=True)
  
  def __str__(self):
      return self.name_singular
  
    
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
  

class Inventory(models.Model):
  store=models.ForeignKey(Store,related_name='inventory',on_delete=models.CASCADE)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()

  def __str__(self):
      return self.name
  

class Purchase(models.Model):
  inventory=models.ForeignKey(Inventory,related_name='purchases',on_delete=models.CASCADE)
  quantity=models.IntegerField()
  purchase_price=models.FloatField()
  sale_price=models.FloatField()
  currency=models.ForeignKey(Currency,related_name='purchases',on_delete=models.CASCADE)
  
  def get_purchase_price(self):
    return f"{self.purchase_price} {self.inventory.store.currency.code}"
  
  def get_sale_price(self):
    return f"{self.sale_price} {self.currency.code}"

  def __str__(self):
      return f"{self.inventory.name} -> Purchase {self.purchase_price}x{self.quantity}"

class Order(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
  draft=models.BooleanField()
  
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

  def __str__(self):
      return f"{self.purchase.inventory.name} -> Sale {self.sale_price}x{self.quantity}"