from django.conf.urls import handler500
from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.LogInView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]

handler404 = views.custom_404_view
handler500 = views.custom_500_view