from django.urls import path
from .views import register, user_login, edit

urlpatterns = [
    #path("signup/", SignUp.as_view(), name="signup"), #/home/signup
    path('register/', register, name='signup'),
    path('login/', user_login, name='login'),
    path('edit/', edit, name='edit'),
]