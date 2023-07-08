from django.urls import path
from yookassa_app.views import status

urlpatterns = [
    path('status/', status),
]