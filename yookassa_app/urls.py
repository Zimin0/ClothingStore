from django.urls import path
from yookassa_app.views import main, create

urlpatterns = [
    path('', main),
    path('create/', create)
]