import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.contrib.auth.models import Permission
# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email salah!'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Email sudah digunakan!'},status=409)
        return JsonResponse({'email_valid':True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Nama tidak boleh ada simbol!'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Nama sudah ada!'},status=409)
        return JsonResponse({'username_valid':True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       context={
        'fieldValues':request.POST
       }
       if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request, 'Kata Sandi terlalu pendek!')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username,email=email,)
                user.set_password(password)
                user.save()
                                
                messages.success(request, 'Akun Berhasil Dibuat!')
                return render(request, 'authentication/register.html')

       return render(request, 'authentication/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username=request.POST['username']
        password=request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Halo ' +user.username+', Anda sudah masuk ke UMKMBOOKEEPING.')
                    return redirect('pembukuan')
                messages.error(request, 'Akun tidak aktif.')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Kredensial tidak valid.')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Mohon isi seluruh form.')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Anda berhasil keluar.')
        return redirect('login')
