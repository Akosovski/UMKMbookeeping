from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('produk', views.index, name="produk"),
    path('tambah-produk', views.tambah_produk, name="tambah-produk"),
    path('ubah-produk/<int:id>', views.ubah_produk, name="ubah-produk"),
    path('hapus-produk/<int:id>', views.hapus_produk, name="hapus-produk"),
    path('cari-produk', csrf_exempt(views.cari_produk), name="cari-produk"),
    path('tambah-vendor', views.tambah_vendor, name="tambah-vendor"),
]