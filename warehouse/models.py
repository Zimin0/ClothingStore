from django.db import models
from pages.models import Product


class Supply(models.Model):
    class Meta:
        verbose_name = 'Поставка товаров'
        verbose_name_plural = 'Поставки товаров'
    
    goods = models.ManyToManyField(Product, verbose_name='Товары', related_name='supply')
    add_date = models.DateTimeField(auto_now_add=True) # дава регистрации поставки

class SupplyItem(models.Model):
    """ """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name='items', help_text="Выберите или создайте товар, который присутствует в данной поствке, и добавьте его кол-во.")
    amount = models.IntegerField(default=1, verbose_name='Кол-во товара' )