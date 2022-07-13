from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="pembukuan"),
    path('detail-umkm', views.detail_umkm, name="detail-umkm"),
    path('ubah-detail', views.ubah_detail, name="ubah-detail"),
    path('tambah-pembukuan', views.tambah_pembukuan, name="tambah-pembukuan"),
    path('ubah-pembukuan/<int:id>', views.ubah_pembukuan, name="ubah-pembukuan"),
    path('hapus-pembukuan/<int:id>', views.hapus_pembukuan, name="hapus-pembukuan"),
    path('cari-pembukuan', csrf_exempt(views.cari_pembukuan), name="cari-pembukuan"),
    path('pembukuan-chart',views.pembukuan_chart, name="pembukuan-chart"),
    path('jual-produk',views.jual_produk, name="jual-produk"),
     path('export-excel', views.export_excel, name="export-excel"),
    path('export-pdf', views.export_pdf, name="export-pdf")
]