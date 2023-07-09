from django.db import models
from pages.models import Product
import datetime

class Discount(models.Model):
    class Meta:
        verbose_name = "Скидка на товары"
        verbose_name_plural = "Скидки на товары"


    def __str__(self) -> str:
        return self.name
    
    name = models.CharField(verbose_name="название скидки", max_length=200, blank=False, default="Скидка")
    percent = models.IntegerField(verbose_name="процент скидки", default=10, blank=False)
    products = models.ManyToManyField(Product, verbose_name="товары на скидку", related_name='discounts', blank=False)
    start_date = models.DateTimeField(verbose_name='конец', help_text='Дата начала действия скидки')
    end_date = models.DateTimeField(verbose_name='конец', help_text='Дата конца действия скидки')

    @property
    def is_expired(self):
        """ Истек ли срок годности скидки."""
        return (self.end_date - datetime.datetime.now(datetime.timezone.utc)).days > 0