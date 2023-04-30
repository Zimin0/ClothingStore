from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# class RegisterForm(UserCreationForm):
#     first_name = forms.CharField(max_length=50, label='Имя', help_text="Будет использоваться при оформлении заказа")
#     second_name = forms.CharField(max_length=50, label='Фамилия', help_text="Будет использоваться при оформлении заказа")
#     address = forms.CharField(max_length=1000, label='Адрес')
#     phone = forms.CharField(max_length=12, label='Тел. номер, напр.: +79313261560')

#     class Meta:
#         model = User
#         fields = ["username", "password1", "password2", "first_name", "second_name", "phone", "email", "address"]



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    


from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone',)
