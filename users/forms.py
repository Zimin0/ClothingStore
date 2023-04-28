from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Имя', help_text="Будет использоваться при оформлении заказа")
    second_name = forms.CharField(max_length=50, label='Фамилия', help_text="Будет использоваться при оформлении заказа")
    address = forms.CharField(max_length=1000, label='Адрес')
    phone = forms.CharField(max_length=12, label='Тел. номер, напр.: +79313261560')

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "second_name", "phone", "email", "address"]