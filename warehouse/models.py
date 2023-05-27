from django.db import models
from pages.models import Product


class Supply(models.Model):
    """ Поставка товаров на склад"""
    class Meta:
        verbose_name = 'Поставка товаров на склад'
        verbose_name_plural = 'Поставки товаров на склад'
    
    def __str__(self):
        return f"Поставка от {self.add_date.strftime('%d.%m.%Y')}"
    
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации поставки") # дата регистрации поставки

class SupplyItem(models.Model):
    class Meta:
        verbose_name = 'Товар из поставки'
        verbose_name_plural = 'Товары из поставки'
    
    def __str__(self):
        return f"Часть поставки №{self.supply_link.id}"

    """ Реализует сочетание товара и его количества. """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name='+', blank=False,  help_text="Товар, пришедший на склад в поствке.")
    amount = models.IntegerField(default=1, verbose_name='Кол-во товара' )
    supply_link = models.ForeignKey(Supply, on_delete=models.CASCADE, verbose_name="Ссылка на поставку", blank=False, related_name='sup_item')
    
    # def update_products_amount(self):
    #     """ Добавляет к товарам кол-во пришедших с поставкой. """
    #     pass