from django.forms import ValidationError
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required  
from .forms import LoginForm, UserRegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


@login_required
def edit(request):
    # Лучше перенести валидацию в clean_<field_name> в forms.py
    def phone_is_exists(request) -> bool:
        """Введенный телефон уже существует."""
        try:
            profile = Profile.objects.get(phone=request.POST['phone']) # has_changed()
            return (request.user.profile.id != profile.id) # Если пользователь оставил в форме неизмененный номер телефона - то все окей.
        except Profile.DoesNotExist:
            return False
        
    context = {}

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if phone_is_exists(request):
            profile_form.add_error('phone', 'Пользователь с таким телефоном уже существует!')
            return render(request, 'registration/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #messages.success(request, 'Данные сохранены!')
            return redirect('pages:profile')
        else:
            return render(request,
                  'registration/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
        #return redirect('pages:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'registration/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
