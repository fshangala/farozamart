from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from store.models import Store

# Create your models here.
gender_options = (
  ('Male','Male'),
  ('Female','Female')
)
class Profile(models.Model):
  user=models.OneToOneField(to=User,on_delete=models.CASCADE,related_name='profile')
  phone=models.CharField(max_length=20,null=True)
  gender=models.CharField(max_length=200,choices=gender_options,default='Male')
  address=models.CharField(max_length=200,null=True)
  is_seller=models.BooleanField(default=False)
  is_reseller=models.BooleanField(default=False)
  picture=models.ImageField(upload_to='profile/pictures',default='profile/default.png')
  
  def full_name(self):
    return f"{self.user.first_name} {self.user.last_name}"
  
  @receiver(post_save, sender=User)
  def _post_save_receiver(sender, instance, created, **kwargs):
    if(created):
      Profile.objects.create(user=instance)
    else:
      instance.profile.save()