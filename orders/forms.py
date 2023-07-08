from django import forms
from .models import Order
from pages.models import Promocode
from users.models import Profile
from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)

class OrderCreateForm(forms.ModelForm):
    promocode = forms.CharField(label='Промокод', required=False)
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal_code']
    
    def clean_promocode(self):
        data = self.cleaned_data
        

        if data['promocode'] == '':
            return data['promocode']
        
        try:
            cur_promo = Promocode.objects.get(code=data['promocode']) # ищем введенный промокод в БД
            if Profile.objects.get(phone=data['phone']).user == cur_promo.user:
                logger.warning(f"Пользователь {cur_promo.user} воспользовался своим же промокодом.")
                raise forms.ValidationError('Нельзя использовать свой промокод!')  
            if cur_promo.is_valid(): # Не истек ли срок годности промокода.
                logger.warning(f"Промокод {data['promocode']} существует.")
            else:
                logger.warning(f"Срок промокода {data['promocode']} истек.")
                raise forms.ValidationError('Срок промокода уже истек!')  
        except Promocode.DoesNotExist:
            logger.warning(f"Нет промокода {data['promocode']}.")
            raise forms.ValidationError('Такого промокода не существует!')
        
        return data['promocode']