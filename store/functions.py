from django.contrib.auth.models import User
from store import models
from django.shortcuts import get_object_or_404
from dropshipping.functions import steadfastCreateOrder

def getUserPurchases(user:User):
  inventory = user.store.inventory.all()
  qs=models.Purchase.objects.none()
  for a in inventory:
    if qs:
      qs = qs.union(a.purchases.all())
    else:
      qs = a.purchases.all()

  return qs

def getUserActivePurchases(user:User):
  inventory = user.store.inventory.all()
  qs=models.Purchase.objects.none()
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
    
  qs1=models.Sale.objects.none()
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

def HTMLInvoice(order:models.Order):
  html='<html><head>'
  html+=f'<title>Invoice #{order.id}</title>'
  html+='<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">'
  html+='</head></html>'
  html+='</head></html>'
  
  return html