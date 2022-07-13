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
def cari_produk(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        produks = Produk.objects.filter(
            sellprice__istartswith=search_str, owner=request.user) | Produk.objects.filter(
            dateadded__istartswith=search_str, owner=request.user) | Produk.objects.filter(
            name__icontains=search_str, owner=request.user) | Produk.objects.filter(
            vendor__icontains=search_str, owner=request.user) | Produk.objects.filter(
            stock__istartswith=search_str, owner=request.user) 
        data = produks.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url = '/authentication/login')
def index(request):
    vendors = Vendor.objects.all()
    produks = Produk.objects.all()
    paginator = Paginator(produks, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
       'produks': produks,
       'page_obj': page_obj,
    }
    return render(request, 'produk/index.html', context) 

@login_required(login_url = '/authentication/login')
def tambah_produk(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    if request.method == 'GET':
        return render(request, 'produk/tambah_produk.html', context)

    if request.method == 'POST':
        name = request.POST.get('name')
        buyprice = request.POST.get('buyprice')
        sellprice = request.POST.get('sellprice')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        dateadded = request.POST.get('dateadded')
        dateupdated = request.POST.get('dateadded')
        vendor = request.POST.get('vendor')

        if not name:
            messages.error(request, 'Nama Produk perlu diisi.')
            return render(request, 'produk/tambah_produk.html', context)

        if not buyprice:
            messages.error(request, 'Harga Beli perlu diisi.')
            return render(request, 'produk/tambah_produk.html', context)

        if not sellprice:
            messages.error(request, 'Harga Jual perlu iisi.')
            return render(request, 'produk/tambah_produk.html', context)

        if not description:
            messages.error(request, 'Deskripsi perlu diisi.')
            return render(request, 'produk/tambah_produk.html', context)

        if not stock:
            messages.error(request, 'Stok perlu diisi.')
            return render(request, 'produk/tambah_produk.html', context)

        if not dateadded:
            messages.error(request, 'Tanggal Pengadaan perlu diisi.')
            return render(request, 'produk/tambah_produk.html', context)

        # Date Updated Sama Dengan Date Added Karena Awal Produk Masuk
        Produk.objects.create(owner=request.user, name=name, buyprice=buyprice, sellprice=sellprice, description=description, stock=stock, dateadded=dateadded, dateupdated=dateadded, vendor=vendor)
        messages.success(request, 'Penambahan Produk Sukses.')

        return redirect('produk')

@login_required(login_url = '/authentication/login')
def ubah_produk(request, id):
    produks = Produk.objects.get(pk=id)
    vendors = Vendor.objects.all() 
    context = {
        'produks': produks,
        'values': produks,
        'vendors': vendors
    }
    if request.method == 'GET':
        return render(request, 'produk/ubah_produk.html', context)
        
    if request.method == 'POST':
        name = request.POST.get('name')
        buyprice = request.POST.get('buyprice')
        sellprice = request.POST.get('sellprice')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        dateupdated = request.POST.get('dateupdated')
        vendor = request.POST.get('vendor')

        if not name:
            messages.error(request, 'Nama Produk perlu diisi.')
            return render(request, 'produk/ubah_produk.html', context)

        if not buyprice:
            messages.error(request, 'Harga Beli perlu diisi.')
            return render(request, 'produk/ubah_produk.html', context)

        if not sellprice:
            messages.error(request, 'Harga Jual perlu iisi.')
            return render(request, 'produk/ubah_produk.html', context)

        if not description:
            messages.error(request, 'Deskripsi perlu diisi.')
            return render(request, 'produk/ubah_produk.html', context)

        if not stock:
            messages.error(request, 'Stok perlu diisi.')
            return render(request, 'produk/ubah_produk.html', context)
        
        if not dateupdated:
            messages.error(request, 'Tanggal Perubahan perlu diisi.')
            return render(request, 'produk/ubah_produk.html', context)
        
        produks.owner = request.user
        produks.name = name
        produks.buyprice = buyprice
        produks.sellprice = sellprice
        produks.description = description
        produks.stock = stock
        produks.dateupdated = dateupdated
        produks.vendor = vendor

        produks.save()
        messages.success(request, 'Perubahan Produk Sukses.')

        return redirect('produk')

def hapus_produk(request, id):
    produk = Produk.objects.get(pk=id)
    produk.delete()

    messages.success(request, 'Produk Berhasil Terhapus.')
    return redirect('produk')

@login_required(login_url = '/authentication/login')
def tambah_vendor(request):
    vendors = Vendor.objects.all()
    context = {
       'vendors': vendors,
    }
    if request.method == 'GET':
        return render(request, 'produk/tambah_vendor.html', context) 
        
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')

        if not name:
            messages.error(request, 'Nama Vendor perlu diisi.')
            return render(request, 'produk/tambah_vendor.html', context)

        if not address:
            messages.error(request, 'Alamat Vendor perlu diisi.')
            return render(request, 'produk/tambah_vendor.html', context)
        
        Vendor.objects.create(name=name, address=address)
        messages.success(request, 'Penambahan Vendor Sukses.')

        return redirect('produk')