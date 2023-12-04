from django.contrib import admin
from paymentgateway import models

# Register your models here.
admin.site.register(models.Transaction)