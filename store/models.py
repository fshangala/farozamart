from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Store(models.Model):
  user=models.OneToOneField(User,related_name='store',on_delete=models.CASCADE)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()

  def __str__(self):
      return self.name
  

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

  def __str__(self):
      return f"{self.inventory.name} -> Purchase {self.purchase_price}x{self.quantity}"
  

class Sale(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
  purchase=models.ForeignKey(Purchase,related_name='sales',on_delete=models.CASCADE)
  quantity=models.IntegerField()
  sale_price=models.FloatField()

  def __str__(self):
      return f"{self.purchase.inventory.name} -> Sale {self.sale_price}x{self.quantity}"