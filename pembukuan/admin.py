from django.contrib import admin
from .models import Pembukuan, Category

# Register your models here.
admin.site.register(Pembukuan)
admin.site.register(Category)