from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pages.models import Promocode

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', null=True, unique=True)
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

''' 
А теперь установим сигналы для Profile на автоматическое создание/обновление, 
когда мы создаем/обновляем стандартную модель пользователя (User):

<h2>{{ user.get_full_name }}</h2>
<ul>
  <li>Имя пользователя: {{ user.username }}</li>
  <li>Местоположение: {{ user.profile.location }}</li>
  <li>Дата рождения: {{ user.profile.birth_date }}</li>
</ul>

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()
'''