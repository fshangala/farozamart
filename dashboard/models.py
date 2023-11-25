from django.db import models

class Option(models.Model):
  name=models.CharField(max_length=200)
  value=models.TextField()

  def __str__(self):
      return self.name
  