from django.contrib.auth.models import User
from store import models
from django.shortcuts import get_object_or_404
from dropshipping.functions import steadfastCreateOrder

def getUserPurchases(user:User):
  inventory = user.store.inventory.all()
  qs=None
  for a in inventory:
    if qs:
      qs = qs.union(a.purchases.all())
    else:
      qs = a.purchases.all()

  return qs

def getUserActivePurchases(user:User):
  inventory = user.store.inventory.all()
  qs=None
  for a in inventory:
    if qs:
      qs = qs.union(a.purchases.filter(quantity__gt=0))
    else:
      qs = a.purchases.all()

  return qs

def getUserResalePurchases(user:User):
  return user.resales.all()

def getUserSales(user:User):
  qs = getUserPurchases(user)
    
  qs1=None
  for b in qs:
    if qs1:
      qs1 = qs1.union(b.sales.all())
    else:
      qs1 = b.sales.all()
  
  return qs1

def CODPayment(pk) -> models.Order:
  order = get_object_or_404(models.Order,pk=pk)
  for item in order.sales.all():
    item.cart = False
    item.save()
      
  order.draft = False
  order.save()
  
  steadfastCreateOrder(order)
  
  return order