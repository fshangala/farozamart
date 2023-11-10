from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Store(models.Model):
  user=models.ForeignKey(User,related_name='stores',on_delete=models.CASCADE)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()

class Inventory(models.Model):
  store=models.ForeignKey(Store,related_name='inventory',on_delete=models.CASCADE)
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()

class Purchase(models.Model):
  inventory=models.ForeignKey(Inventory,related_name='purchase',on_delete=models.CASCADE)
  quantity=models.IntegerField()
  purchase_price=models.FloatField()
  sale_price=models.FloatField()

class Sale(models.Model):
  inventory=models.ForeignKey(Inventory,related_name='sales',on_delete=models.CASCADE)
  quantity=models.IntegerField()
  sale_price=models.FloatField()