from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Produk(models.Model):
    name = models.CharField(max_length=255)
    buyprice = models.FloatField()
    sellprice = models.FloatField()
    description = models.TextField()
    dateadded = models.DateField(default=now)
    dateupdated = models.DateField(default=now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    vendor = models.CharField(max_length=255)
    stock = models.IntegerField(default=1)

    def __str__(self):
        return self.vendor

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    # company = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Vendors'