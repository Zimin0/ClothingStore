from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from decimal import Decimal

class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self): # Надо поменять 
        return f'Профиль пользователя {self.user}' 
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', null=True, unique=True, help_text='Номер телефона в формате +79112345678')
    address = models.CharField(max_length=300, verbose_name="Адрес доставки", blank=True, null=True)
    linked_to_promer = models.ForeignKey(User, 
                                        on_delete=models.CASCADE, 
                                        related_name="promo_owner_linked_to", 
                                        verbose_name='Владелец промокода', 
                                        help_text='Владелец промокода, к которому привязан этот редактируемый пользователь. Поле может быть пустым.', 
                                        blank=True, 
                                        null=True, 
                                        default=None)
    bought_already = models.BooleanField(verbose_name="Была ли совершена хотя бы 1 покупка", default=False)
    card16 = models.CharField(max_length=16 ,verbose_name="Номер карты", help_text='16 цифр на банковской карте', blank=True, null=True)
    points = models.DecimalField(
        verbose_name="Баллы партнерской программы",
        default=0,
        max_digits=7, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    
    def already_bought(self) -> bool:
        """ Покупал ли юзер ранее."""
        return self.bought_already
    
    def already_put_promo(self):
        """ Вводил ли юзер промокод ранее."""
        return self.linked_to_promer != None
        
        
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