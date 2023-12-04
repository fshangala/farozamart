from django.db import models

# Create your models here.
class Transaction(models.Model):
  transaction_id=models.CharField(max_length=200,unique=True)
  amount=models.FloatField()
  
  def __str__(self):
      return self.transaction_id
  