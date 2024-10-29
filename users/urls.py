from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.LogInView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]