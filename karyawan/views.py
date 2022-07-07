from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from authentication import views
import json
from django.http import JsonResponse
import datetime

@login_required(login_url = '/authentication/login')
def index(request):
    users = User.objects.all()
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
       'users': users,
       'page_obj': page_obj,
    }
    return render(request, 'karyawan/index.html', context)

@login_required(login_url = '/authentication/login')
def tambah_karyawan(request):
    return render(request, 'karyawan/tambah-karyawan.html')
