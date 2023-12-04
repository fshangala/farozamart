from django.contrib.auth.models import User
from store import models

def getUserPurchases(user:User):
  inventory = user.store.inventory.all()
  qs=None
  for a in inventory:
    if qs:
      qs = qs.union(a.purchases.all())
    else:
      qs = a.purchases.all()

  return qs

def getUserResalePurchases(user:User):
  inventory = user.store.inventory.all()
  qs=None
  for a in inventory:
    if qs:
      qs = qs.union(a.purchases.all())
    else:
      qs = a.purchases.all()

  return qs

def getUserSales(user:User):
  qs = getUserPurchases(user)
    
  qs1=None
  for b in qs:
    if qs1:
      qs1 = qs1.union(b.sales.all())
    else:
      qs1 = b.sales.all()
  
  return qs1