from django.core.exceptions import ValidationError
from store import models

def unique_store_name(value):
  if models.Store.objects.filter(name__iexact=value).exists():
    raise ValidationError(f"The name \'{value}\' is taken")

def unique_inventory_name(value):
  if models.Inventory.objects.filter(name__iexact=value).exists():
    raise ValidationError(f"The name \'{value}\' is taken")