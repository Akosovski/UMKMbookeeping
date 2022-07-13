from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from pembukuan.models import Category, Details

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    company = models.ForeignKey(Details, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Vendors'

class Produk(models.Model):
    name = models.CharField(max_length=255)
    buyprice = models.FloatField()
    sellprice = models.FloatField()
    description = models.TextField()
    dateadded = models.DateField(default=now)
    dateupdated = models.DateField(default=now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    company = models.ForeignKey(Details, on_delete=models.SET_NULL, blank=True, null=True)
    vendor = models.CharField(max_length=255)
    stock = models.IntegerField(default=1)
    vend = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.vendor