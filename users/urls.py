from django.urls import path
from .views import home, SignUp
urlpatterns = [
    path('', home, name="home"), # /home/
    path("signup/", SignUp.as_view(), name="signup"), #/home/signup
]