from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  user=models.OneToOneField(to=User,on_delete=models.CASCADE,related_name='profile')
  phone=models.CharField(max_length=20)