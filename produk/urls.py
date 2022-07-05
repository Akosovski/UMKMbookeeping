from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('produk', views.index, name="produk"),
    path('tambah-produk', views.tambah_produk, name="tambah-produk"),
    path('ubah-produk/<int:id>', views.ubah_produk, name="ubah-produk"),
]