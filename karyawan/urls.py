from django.urls import path
from . import views
from authentication.views import RegistrationView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('karyawan', views.index, name="karyawan"),
    path('tambah-karyawan', RegistrationView.as_view(), name="tambah-karyawan"),
]