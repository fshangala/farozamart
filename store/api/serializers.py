from rest_framework import serializers
from store import models
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