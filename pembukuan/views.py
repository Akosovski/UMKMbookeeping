from django.contrib.auth.decorators import login_required
from multiprocessing import context
from .models import Category, Pembukuan
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

def cari_pembukuan(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        pembukuans = Pembukuan.objects.filter(
            subtotal__istartswith=search_str, owner=request.user) | Pembukuan.objects.filter(
            date__istartswith=search_str, owner=request.user) | Pembukuan.objects.filter(
            description__icontains=search_str, owner=request.user) | Pembukuan.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = pembukuans.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url = '/authentication/login')
def index(request):
    categories = Category.objects.all()
    pembukuans = Pembukuan.objects.filter(owner=request.user)
    paginator = Paginator(pembukuans, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'pembukuans': pembukuans,
        'page_obj': page_obj,
    }
    return render(request, 'pembukuan/index.html', context)

@login_required(login_url = '/authentication/login')
def tambah_pembukuan(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'pembukuan/tambah_pembukuan.html', context)

    if request.method == 'POST':
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        tax = request.POST.get('tax')
        subtotal = request.POST.get('subtotal')
        date = request.POST.get('date')

        if not description:
            messages.error(request, 'Deskripsi perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        if not price:
            messages.error(request, 'Jumlah perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        if not tax:
            messages.error(request, 'Pajak dinolkan apabila tidak diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        if not subtotal:
            messages.error(request, 'Total perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        if not date:
            messages.error(request, 'Tanggal perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        Pembukuan.objects.create(owner=request.user, price=price, tax=tax, subtotal=subtotal, description=description, category=category, date=date)
        messages.success(request, 'Penambahan Pembukuan Sukses.')

        return redirect('pembukuan')

@login_required(login_url = '/authentication/login')
def ubah_pembukuan(request, id):
    pembukuans = Pembukuan.objects.get(pk=id)
    categories = Category.objects.all() 
    context = {
        'pembukuans': pembukuans,
        'values': pembukuans,
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'pembukuan/ubah_pembukuan.html', context)
        
    if request.method == 'POST':
        price = request.POST.get('price')
        tax = request.POST.get('tax')
        subtotal = request.POST.get('subtotal')

        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('date')

        if not description:
            messages.error(request, 'Deskripsi perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        if not price:
            messages.error(request, 'Jumlah perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        if not tax:
            messages.error(request, 'Pajak dinolkan apabila tidak diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        if not subtotal:
            messages.error(request, 'Total perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)

        if not date:
            messages.error(request, 'Tanggal perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html', context)
        
        pembukuans.owner = request.user
        pembukuans.price = price
        pembukuans.date = date
        pembukuans.category = category
        pembukuans.description = description
        pembukuans.tax = tax
        pembukuans.subtotal = subtotal

        pembukuans.save()
        messages.success(request, 'Perubahan Pembukuan Sukses.')

        return redirect('pembukuan')

def hapus_pembukuan(request, id):
    pembukuan = Pembukuan.objects.get(pk=id)
    pembukuan.delete()

    messages.success(request, 'Pembukuan Berhasil Terhapus.')
    return redirect('pembukuan')