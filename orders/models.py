from django.db import models
from pages.models import Product
from pages.models import Promocode


class Order(models.Model):
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Оформленный заказ'
        verbose_name_plural = 'Оформленные заказы'

    STATUS = (
        ('OS', 'Без статуса'),
        ('OTW', 'На пути к заказчику'),
        ('RE', 'Отменен'),
        ('FI', 'Завершен'),
    )

    PAYMENT = (
        ('ON', 'Оплачен онлайн'),
        ('NA', 'Отказ в онлайн оплате'),
        ('OF', 'Оплачен оффлайн'),
        ('NP', 'Еще не оплачен'),
    )

    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True)
    email = models.EmailField(verbose_name='Электронный адрес', null=True)
    phone = models.CharField(max_length=12, verbose_name="Номер телефона", null=True, blank=False, unique=True)
    address = models.CharField(max_length=250, verbose_name='Адрес', null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="Почтовый индекс" )
    promocode_used = models.ForeignKey(Promocode, on_delete=models.SET_NULL, verbose_name="Использованный промокод", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name="Оплачен")
    status = models.CharField(max_length=3, choices=STATUS, default='OS', null=True, verbose_name='Статус')
    payment_status = models.CharField(max_length=2, verbose_name='Как оплачен заказ?', choices=PAYMENT, default='NP')
        
    def process_the_order(self, user):
        """ 
        Обрабатывает заказ согласно схеме. 
        Возвращает, что нужно сделать/начислить/тп
        """
        data = {
            'customer': None,
            'seller': None,
            'message': None
        }

        if not(user.profile.already_bought()): # если пользователь ранее не совершал покупки
            if not(self.does_promo_used()): # если при покупке не был введен промокод
                # занести юзера в бд (ххх)
                pass
            else: # если при покупке был введен промокод
                data['customer'] = 'discount10' # (хх+)
                data['seller'] = 'bonus09'
        else: # если пользователь ранее совершал покупки
            if not(self.does_promo_used_early(user)): # если покупатель еще не привязан к промокоду
                if not(self.does_promo_used()): # если при покупке не был введен промокод
                    # Вы уже покупали у нас # (+хх)
                    data['message'] = 'Кажется, Вы уже покупали у нас!'
                    pass
                else: # если при покупке был введен промокод
                    data['customer'] = 'discount10' # (+х+)
            else: # если покупатель уже привязан к промокоду 
                if not(self.does_promo_used()): # если при покупке не был введен промокод
                    data['seller'] = 'bonus01' # (++x)
                else:
                    data['customer'] = 'discount10' # (+++)
                    data['seller'] = 'bonus09'



    def __str__(self): # Надо поменять 
        return 'Заказ №{}'.format(self.id) 

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def does_promo_used(self) -> bool:
        """ Введен ли промокод в данном заказе. """
        return not(self.promocode_used is None)

    def does_promo_used_early(self, user):
        """ Привязан ли данный покупатель к промокоду. """
        return not(user.profile.linked_to_promer is None)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
