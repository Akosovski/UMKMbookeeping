from multiprocessing import context
from django.contrib.auth.decorators import login_required
from .models import Category, Pembukuan
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

@login_required(login_url = '/authentication/login')
# Create your views here.
def index(request):
    categories = Category.objects.all()
    pembukuan = Pembukuan.objects.filter(owner=request.user)
    paginator = Paginator(pembukuan, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'pembukuan': pembukuan,
        'page_obj': page_obj,
    }
    return render(request, 'pembukuan/index.html', context)

def tambah_pembukuan(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'pembukuan/tambah_pembukuan.html', context)

    if request.method == 'POST':
        amount = request.POST.get['amount']
        description = request.POST.get['description']
        category = request.POST.get['category']
        date = request.POST.get['date']

        if not amount:
            messages.error(request, 'Jumlah perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html')

        if not description:
            messages.error(request, 'Deskripsi perlu diisi.')
            return render(request, 'pembukuan/tambah_pembukuan.html')

        Pembukuan.objects.create(owner=request.user, amount=amount, description=description, category=category, date=date)
        messages.success(request, 'Penambahan Pembukuan Sukses.')

        return redirect('tambah-pembukuan')

def ubah_pembukuan(request, id):
    pembukuan = Pembukuan.objects.get(pk=id)
    context = {
        'pembukuan': pembukuan,
        'values': pembukuan,
        'categories': pembukuan,
    }
    if request.method == 'GET':
        return render(request, 'pembukuan/ubah-pembukuan.html', context)
    if request.method == 'GET':
        amount = request.POST.get['amount']
        description = request.POST.get['description']
        category = request.POST.get['category']
        date = request.POST.get['date']

        if not amount:
            messages.error(request, 'Jumlah perlu diisi.')
            return render(request, 'pembukuan/ubah_pembukuan.html')

        if not description:
            messages.error(request, 'Deskripsi perlu diisi.')
            return render(request, 'pembukuan/ubah_pembukuan.html')

        pembukuan.owner = request.user
        pembukuan.amount = amount
        pembukuan.date = date
        pembukuan.category = category
        pembukuan.description = description

        Pembukuan.save()
        messages.success(request, 'Perubahan Pembukuan Sukses.')

        return render(request, 'pembukuan/ubah-pembukuan.html', context)