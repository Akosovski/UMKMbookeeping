from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import datetime

@login_required(login_url = '/authentication/login')
def index(request):
    return render(request, 'karyawan/index.html')

@login_required(login_url = '/authentication/login')
def tambah_karyawan(request):
    return render(request, 'karyawan/tambah-karyawan.html')