from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Pembukuan(models.Model):
    price = models.FloatField()
    tax = models.FloatField()
    subtotal = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'