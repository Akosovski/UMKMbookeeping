from django.contrib.auth.decorators import login_required
from multiprocessing import context
from .models import Vendor, Produk
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

# Create your views here.
@login_required(login_url = '/authentication/login')
def index(request):
    # vendors = Vendor.objects.all()
    # produks = Produk.objects.filter(owner=request.user)
    # paginator = Paginator(produks, 5)
    # page_number = request.GET.get('page')
    # page_obj = Paginator.get_page(paginator, page_number)
    # context = {
    #    'produks': produks,
    #    'page_obj': page_obj,
    # }
    return render(request, 'produk/index.html') #, context