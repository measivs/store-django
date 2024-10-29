from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserCreationForm
from django.contrib import messages

# Create your views here.

class LogInView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            print(f"User authenticated: {user.email}")
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register.html'  # Your template for registration
    success_url = reverse_lazy('login')
