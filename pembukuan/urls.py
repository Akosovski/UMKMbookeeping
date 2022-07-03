from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="pembukuan"),
    path('tambah-pembukuan', views.tambah_pembukuan, name="tambah-pembukuan"),
    path('ubah-pembukuan/<int:id>', views.ubah_pembukuan, name="ubah-pembukuan"),
    path('hapus-pembukuan/<int:id>', views.hapus_pembukuan, name="hapus-pembukuan"),
]