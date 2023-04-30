from django.urls import path
from .views import register, user_login, edit, profile

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    #path('login/', user_login, name='login'),
    path('edit/', edit, name='edit'),
    path('profile/', profile, name='profile'),
]