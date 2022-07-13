from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser, AbstractUser
from django.utils.timezone import now
from phone_field import PhoneField

# Create your models here.


class Details(models.Model):
    name = models.CharField(max_length=255)
    pemilik = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = PhoneField(blank=True)
    field = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = 'Categories'

class Pembukuan(models.Model):
    price = models.FloatField()
    tax = models.FloatField(blank=True, null=True)
    subtotal = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    company = models.ForeignKey(Details, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.CharField(max_length=255)
    profit = models.FloatField(blank=True, null=True)
    categ = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.category