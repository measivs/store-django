from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserCreationForm
# Create your views here.

class LogInView(LoginView):
    template_name = 'login.html'

class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register.html'  # Your template for registration
    success_url = reverse_lazy('login')
