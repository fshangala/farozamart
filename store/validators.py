from django.core.exceptions import ValidationError
from store import models

def unique_store_name(value):
  if models.Store.objects.filter(name__iexact=value).exists():
    raise ValidationError(f"The name \'{value}\' is taken")

def unique_inventory_name(value):
  if models.Inventory.objects.filter(name__iexact=value).exists():
    raise ValidationError(f"The name \'{value}\' is taken")

class CurrencyValidators:
  def unique_symbo(value):
    if models.Currency.objects.filter(symbol__iexact=value).exists():
      raise ValidationError(f"The symbo {value} is taken")
  
  def unique_code(value):
    if models.Currency.objects.filter(code__iexact=value).exists():
      raise ValidationError(f"The code {value} is taken")