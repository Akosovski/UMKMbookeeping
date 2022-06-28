from django.urls import path
from .views import RegistrationView, LoginView,  UsernameValidationView, EmailValidationView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('register', RegistrationView.as_view(), name="register"),
    path('username-validation', csrf_exempt(UsernameValidationView.as_view()), 
        name="username-validation"),
    path('email-validation', csrf_exempt(EmailValidationView.as_view()),
        name="email-validation")
]