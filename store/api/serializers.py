from rest_framework import serializers
from store import models
from accounts.api.serializers import UserSerializer
from django.contrib.auth.models import User

class CurrencySerializer(serializers.ModelSerializer):
  class Meta:
    model=models.Currency
    fields="__all__"
    
class StoreSerializer(serializers.ModelSerializer):
  class Meta:
    model=models.Store
    fields="__all__"

class InventorySerializer(serializers.ModelSerializer):
  class Meta:
    model=models.Inventory
    fields="__all__"

class PurchaseSerializer(serializers.ModelSerializer):
  inventory=InventorySerializer()
  currency=CurrencySerializer()
  class Meta:
    model=models.Purchase
    fields=[
      "id",
      "inventory",
      "quantity",
      "purchase_price",
      "sale_price",
      "resale_price",
      "currency",
      "get_sale_price"
    ]

class AddToCartSerializer(serializers.Serializer):
  quantity=serializers.IntegerField()

  def __init__(self,user:User,listing:models.Purchase,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.user=user
    self.listing=listing
  
  def save(self):
    try:
      order=self.user.orders.get(draft=True)
    except Exception as e:
      order=models.Order.objects.create(user=self.user,draft=True)
      
    current = models.Sale.objects.filter(user=self.user,purchase=self.listing,cart=True).first()
    if current:
      current.quantity += self.validated_data['quantity']
      current.save()
    else:
      sale = models.Sale.objects.create(
        user=self.user,
        purchase=self.listing,
        quantity=self.validated_data['quantity'],
        sale_price=self.listing.sale_price,
        order=order,
        cart=True,
        approved=False
      )

class OrderSalesSerializer(serializers.ModelSerializer):
  user=UserSerializer()
  purchase=PurchaseSerializer()
  class Meta:
    model=models.Sale
    fields=[
      "id",
      "user",
      "purchase",
      "quantity",
      "sale_price",
      "get_sale_price",
      "cart",
      "approved",
    ]
class OrderSerializer(serializers.ModelSerializer):
  user=UserSerializer()
  sales=OrderSalesSerializer(many=True)
  class Meta:
    model=models.Order
    fields=[
      "id",
      "draft",
      "user",
      "transaction",
      "sales",
      "total_cost",
      "total_cost_number",
    ]

class SalesSerializer(serializers.ModelSerializer):
  user=UserSerializer()
  purchase=PurchaseSerializer()
  order=OrderSerializer()
  class Meta:
    model=models.Sale
    fields=[
      "id",
      "user",
      "purchase",
      "quantity",
      "sale_price",
      "get_sale_price",
      "order",
      "cart",
      "approved",
    ]