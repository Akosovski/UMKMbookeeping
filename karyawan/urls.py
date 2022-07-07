from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('karyawan', views.index, name="karyawan"),
    path('tambah-karyawan', views.tambah_karyawan, name="tambah-karyawan"),
]