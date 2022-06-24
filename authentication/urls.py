from django.urls import path
from .views import RegistrationView, LoginView


urlpatterns = [
    path('login', LoginView.as_view(), name="register"),
    path('register', RegistrationView.as_view(), name="register")
]