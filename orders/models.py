from django.db import models
from django.contrib.auth.models import User
from pages.models import Product, Promocode
from django.core.validators import MinValueValidator
from decimal import Decimal

import logging
logger = logging.getLogger(__name__)

class Order(models.Model):
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Оформленный заказ'
        verbose_name_plural = 'Оформленные заказы'

    STATUS = (
        ('OS', 'Без статуса'),
        ('OTW', 'На пути к заказчику'),
        ('RTP', 'Ожидает оплаты'),
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
    phone = models.CharField(max_length=12, verbose_name="Номер телефона", null=True, blank=False)
    address = models.CharField(max_length=250, verbose_name='Адрес', null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="Почтовый индекс" )
    promocode_used = models.ForeignKey(Promocode, on_delete=models.SET_NULL, verbose_name="Использованный промокод", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name="Оплачен")
    status = models.CharField(max_length=3, choices=STATUS, default='OS', null=True, verbose_name='Статус')
    payment_status = models.CharField(max_length=2, verbose_name='Как оплачен заказ?', choices=PAYMENT, default='NP')
    total_price = models.DecimalField(
        verbose_name="Стоимость",
        help_text='Окончательная стоимость с учетом всех скидок и комиссий, которую заплатит покупатель',
        default=0,
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
        
    def process_the_order(self, user:User, price:float, promo_percent:int, promo_owner:User, promo_pk:int) -> dict:
        """ 
        Обрабатывает заказ согласно схеме. 
        Возвращает, что нужно сделать/начислить/т.п.
        * user - покупатель
        * price - чистая цена корзины товаров
        * promo_percent - скидка с промокода в процентах
        * promo_owner - владелец промокода
        * pk промокода
        """

        points_to_promo_owner = 0 # кол-во баллов, которые будут начислены владельцу промокода.
        total_price = 0 # будет записано в Order объект
        total_price += price # чистая сумма товаров в корзине
        total_price += Order.get_yookassa_commission(price) # добавляем в суммарную цену комиссию юкассы


        if not(user.profile.already_bought()): # если пользователь ранее не совершал покупки
            print(f'{user} ранее не совершал покупки')
            user.profile.bought_already = True  
            user.save() 
            print(f'Для {user} отмечено, что он покупал ранее.')  
            if not(self.does_promo_used()): # если при этой покупке не был введен промокод
                # занести юзера в бд (ххх) ??????????????????????
                print(f'{user} при покупке не был введен промокод')
                print('(ххх)')

            else: # если при этой покупке был введен промокод
                total_price -= Order.get_promo_discout(price, promo_percent) # data['customer'] = 'discount10' 
                points_to_promo_owner += Order.get_bonus09(price) # data['seller'] = 'bonus09'
                user.profile.linked_to_promer = Promocode.objects.get(pk=promo_pk).user # привязываем текущего пользователя к промокоду
                print(f'{user} при покупке был введен промокод')
                print('(хх+)')

        else: # если пользователь ранее совершал покупки
            print(f'{user} ранее совершал покупки')
            if not(self.does_promo_used_early(user)): # если покупатель еще не привязан к промокоду
                print(f'{user} еще не привязан к промокоду')
                if not(self.does_promo_used()): # если при этой покупке не был введен промокод
                    # print('Кажется, Вы уже покупали у нас!')
                    print(f'{user} при покупке не был введен промокод')
                    print('(+хх)')

                else: # если при этой покупке был введен промокод
                    total_price -= Order.get_promo_discout(price, promo_percent) 
                    print(f'{user} при покупке был введен промокод')
                    print('(+х+)')

            else: # если покупатель уже привязан к промокоду 
                print(f'{user} уже привязан к промокоду')
                if not(self.does_promo_used()): # если при этой покупке не был введен промокод
                    points_to_promo_owner += Order.get_bonus01(price) 
                    print(f'{user} при покупке не был введен промокод')
                    print('(++x)')

                else: # если при этой покупке был введен промокод
                    total_price -= Order.get_promo_discout(price, promo_percent) 
                    points_to_promo_owner += Order.get_bonus09(price) 
                    print('(+++)')
                    print(f'{user} при покупке был введен промокод')

        return total_price, points_to_promo_owner


    @staticmethod
    def get_yookassa_commission(summ) -> float:
        """ Возвращает кол-во (float) коммиссии Yookassa. """
        comm = 5 # комиссия юкассы в процентах
        return summ * comm / 100

    @staticmethod
    def get_promo_discout(summ, discount:int) -> float:
        """ Возвращает кол-во (float) скидки на заказ. Discount в процентах. """ 
        return summ * discount / 100
    
    @staticmethod
    def get_bonus09(summ):
        return summ * 9 / 100
    
    @staticmethod
    def get_bonus01(summ):
        return summ * 1 / 100
    

    def __str__(self): # Надо поменять 
        return 'Заказ №{}'.format(self.id) 

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def does_promo_used(self) -> bool:
        """ Введен ли промокод в данном заказе. """
        return self.promocode_used is not None

    def does_promo_used_early(self, user):
        """ Привязан ли данный покупатель к промокоду. """
        return user.profile.linked_to_promer is not None


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity




