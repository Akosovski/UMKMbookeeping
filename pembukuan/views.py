from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'pembukuan/index.html')

def tambah_pembukuan(request):
    return render(request, 'pembukuan/tambah_pembukuan.html')