from dataclasses import field
from django.contrib.auth.decorators import login_required
from multiprocessing import context
from .models import Category, Pembukuan, Details
from produk.models import Produk
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import datetime
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

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
    category = Category.objects.all()
    pembukuans = Pembukuan.objects.all()
    paginator = Paginator(pembukuans, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    total_pemasukan = 0
    category_pemasukan = pembukuans.filter(category='Pemasukan')
    for item in category_pemasukan:
        total_pemasukan += item.subtotal
    
    total_pengeluaran = 0
    category_pengeluaran = pembukuans.filter(category='Pengeluaran')
    for item in category_pengeluaran:
        total_pengeluaran += item.subtotal

    total_lain = 0
    category_lain = pembukuans.filter(category='Lain-lain')
    for item in category_lain:
        total_lain += item.subtotal

    context = {
        'pembukuans': pembukuans,
        'page_obj': page_obj,
        'total_pemasukan': total_pemasukan,
        'total_pengeluaran': total_pengeluaran,
        'total_lain': total_lain,
    }
    return render(request, 'pembukuan/index.html', context)

@login_required(login_url = '/authentication/login')
def detail_umkm(request):
    details = Details.objects.all()
    context = {
        'details': details,
    }
    return render(request, 'pembukuan/detail_umkm.html', context)

@login_required(login_url = '/authentication/login')
def ubah_detail(request):
    dynamic_name = ''
    details = Details.objects.get(name=dynamic_name)
    context = {
        'details': details,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        pemilik = request.POST.get('pemilik')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        field = request.POST.get('field')
        address = request.POST.get('address')
        city = request.POST.get('city')

        if not name:
            messages.error(request, 'Nama usaha perlu diisi.')
            return render(request, 'pembukuan/ubah_detail.html', context)

        if not pemilik:
            pemilik = "-"

        if not email:
            messages.error(request, 'Email Perlu diisi.')
            return render(request, 'pembukuan/ubah_detail.html', context)

        if not phone:
            messages.error(request, 'No. Telpon perlu diisi.')
            return render(request, 'pembukuan/ubah_detail.html', context)

        if not field:
            field = "-"
        
        if not address:
            messages.error(request, 'Alamat perlu diisi.')
            return render(request, 'pembukuan/ubah_detail.html', context)

        if not city:
            field = "-"

        dynamic_name = name
        details.name = name
        details.pemilik = pemilik
        details.email = email
        details.phone = phone
        details.field = field
        details.address = address
        details.city = city

        details.save()
        messages.success(request, 'Perubahan Detail Usaha Sukses.')

        return redirect('detail-umkm')
    return render(request, 'pembukuan/ubah_detail.html')

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
        profit=0

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

        Pembukuan.objects.create(owner=request.user, price=price, tax=tax, subtotal=subtotal, description=description, category=category, date=date, profit=profit)
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
            return render(request, 'pembukuan/ubah_pembukuan.html', context)

        if not price:
            messages.error(request, 'Jumlah perlu diisi.')
            return render(request, 'pembukuan/ubah_pembukuan.html', context)

        if not tax:
            messages.error(request, 'Pajak dinolkan apabila tidak diisi.')
            return render(request, 'pembukuan/ubah_pembukuan.html', context)

        if not subtotal:
            messages.error(request, 'Total perlu diisi.')
            return render(request, 'pembukuan/ubah_pembukuan.html', context)

        if not date:
            messages.error(request, 'Tanggal perlu diisi.')
            return render(request, 'pembukuan/ubah_pembukuan.html', context)
        
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

def pembukuan_chart(request):
    todays_date=datetime.date.today()
    six_months_ago=todays_date-datetime.timedelta(days=30*6)
    pembukuans=Pembukuan.objects.filter(date__gte=six_months_ago,date__lte=todays_date)
    finalrep = {}

    def get_category(pembukuan):
        return pembukuan.category

    category_list=list(set(map(get_category, pembukuans)))

    def get_pembukuan_category_subtotal(category):
        subtotal = 0
        filtered_by_category=pembukuans.filter(category=category)

        for item in filtered_by_category:
            subtotal += item.subtotal
        return subtotal

    for x in pembukuans:
        for y in category_list:
            finalrep[y]=get_pembukuan_category_subtotal(y)

    return JsonResponse({'pembukuan_category_data': finalrep}, safe=False)

@login_required(login_url = '/authentication/login')
def jual_produk(request):
    produks = Produk.objects.all()
    if not produks:
        messages.error(request, 'Produk Masih Kosong.')
        return redirect('pembukuan')

    context = {
        'produks': produks
    }
    if request.method == 'GET':
        return render(request, 'pembukuan/jual_produk.html', context)

    if request.method == 'POST':
        name = request.POST.get('produk')
        stock = request.POST.get('stock')
        siproduk_sellprice = Produk.objects.get(name=name)
        price = siproduk_sellprice.sellprice
        buyprice = siproduk_sellprice.buyprice
        profit_raw = price - buyprice
        profit = profit_raw * float(stock)

        category = 'Pemasukan'
        description = 'Penjualan '+ stock +' Buah '+ name

        subtotal = price * int(stock)
        siproduk_stock = Produk.objects.get(name=name)
        intstock = siproduk_stock.stock
        stock_akhir = intstock - int(stock)

        if stock_akhir < 0:
            messages.error(request, 'Stok Produk Tidak Mencukupi.')
            return render(request, 'pembukuan/jual_produk.html', context)

        if not description:
            messages.error(request, 'Deskripsi perlu diisi.')
            return render(request, 'pembukuan/jual_produk.html', context)

        if not stock:
            messages.error(request, 'Stock perlu diisi.')
            return render(request, 'pembukuan/jual_produk.html', context)

        if not subtotal:
            messages.error(request, 'Total perlu diisi.')
            return render(request, 'pembukuan/jual_produk.html', context)

        savedproduks = Produk.objects.get(name__iexact=name)
        savedproduks.stock = stock_akhir
        savedproduks.save()
        Pembukuan.objects.create(owner=request.user, price=price, tax=0, subtotal=subtotal, description=description, category=category, date=datetime.date.today(), profit=profit)
        messages.success(request, 'Penjualan Produk Sukses. Stok telah diperbaharui.')

        return redirect('pembukuan')

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Pembukuan'+ \
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Pembukuan')
    row_num=0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date', 'Description', 'Price in Rp.', 'Tax', 'Category', 'Sub-Total']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows=Pembukuan.objects.values_list(
        'date', 'description', 'price', 'tax', 'category', 'subtotal')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def export_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Pembukuan'+ \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    pembukuans = Pembukuan.objects.all()
    category_pemasukan = Pembukuan.objects.filter(category='Pemasukan')
    sum_pemasukan = 0
    for item in category_pemasukan:
         sum_pemasukan += item.subtotal
    category_pengeluaran = Pembukuan.objects.filter(category='Pengeluaran')
    sum_pengeluaran = 0
    for item in category_pengeluaran:
         sum_pengeluaran += item.subtotal

    html_string = render_to_string(
        'pembukuan/pdf-output.html',{'pembukuans': pembukuans, 'total1': sum_pemasukan, 'total2': sum_pengeluaran})
    html=HTML(string=html_string)

    result=html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response