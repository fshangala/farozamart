from django.contrib import admin
from store import models

# Register your models here.
admin.site.register(models.Inventory)
admin.site.register(models.Purchase)
admin.site.register(models.Sale)