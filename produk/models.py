from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Produk(models.Model):
    name = models.TextField()
    buyprice = models.FloatField()
    sellprice = models.FloatField()
    description = models.TextField()
    dateadded = models.DateField(default=now)
    dateupdated = models.DateField(default=now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    vendor = models.CharField(max_length=255)

    def __str__(self):
        return self.vendor

class Vendor(models.Model):
    vendor = models.CharField(max_length=255)
    vendorname = models.CharField(max_length=255)
    vendoraddress = models.CharField(max_length=255)

    def __str__(self):
        return self.vendor