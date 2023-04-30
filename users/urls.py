from django.urls import path
from .views import register, edit

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
]