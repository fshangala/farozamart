from django.db import models

# Create your models here.
class SteadFastDelivery(models.Model):
  consignment_id=models.IntegerField()
  invoice=models.CharField(max_length=200)
  tracking_code=models.CharField(max_length=200)
  created_at=models.CharField(max_length=200)
  updated_at=models.CharField(max_length=200)
  
  def __str__(self):
      return self.tracking_code