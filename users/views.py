from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from .forms import CustomUserCreationForm, ContactForm
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
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Registration successful! You can now log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ContactView(LoginRequiredMixin, View):
    login_url = '/users/login/'
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"Contact Form Submission from {form.cleaned_data['name']}"
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['email']
            recipient_list = ['mea@mea.com']

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')

        return render(request, self.template_name, {'form': form})


class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request, exception):
    return render(request, '500.html', status=500)
