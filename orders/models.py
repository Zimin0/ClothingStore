from django.db import models
from pages.models import Product
from pages.models import Promocode


class Order(models.Model):
    STATUS = (
        ('RE', 'Отменен'),
        ('OTW', 'На пути к заказчику'),
        ('FI', 'Завершен'),
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
    paid = models.BooleanField(default=False, verbose_name="Ополачен")
    #status = models.CharField(max_length=3, )
    # телефон + промокод
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self): # Надо поменять 
        return 'Заказ №{}'.format(self.id) 

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity



class Purchase(models.Model):
    """ Заказ/покупка """

    class Meta:
        verbose_name = "Запрос на покупку"
        verbose_name_plural = "Запросы на покупки"
    
    STATUS = (
        ('RE', 'Rejected'),
        ('FI', 'Accepted')
    )
    user = ...
    date = ...
    summ = ...
    products = ...
    status = ...
    used_promocode = ...
    address = ...