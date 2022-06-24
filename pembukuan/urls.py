from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="pembukuan"),
    path('tambah-pembukuan', views.tambah_pembukuan, name="tambah-pembukuan")
]