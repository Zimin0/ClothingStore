from django.urls import path
from .views import register, login, edit, profile

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('edit/', edit, name='edit'),
    path('profile/', profile, name='profile'),
]