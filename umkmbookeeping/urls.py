from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('pembukuan.urls')),
    path('authentication/', include('authentication.urls')),
    path('produk/', include('produk.urls')),
    path('karyawan/', include('karyawan.urls')),
    path('admin/', admin.site.urls),
]
