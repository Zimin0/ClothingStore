from django.db import models
import datetime
import string
from random import choice
from django.contrib.auth.models import User


class Category(models.Model):
    """ Категория """
    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"  

    def __str__(self) -> str:
        return f'{self.name}'
    
    name = models.CharField(max_length=100, verbose_name="Название", null=True, blank=False)

class Product(models.Model):
    """ Товар """

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    SEX = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('U', 'Унисекс')
    )

    def __str__(self) -> str:
        return f'id={self.pk} | {self.name}'

    def directory_path(instance, filename) -> str:
        return ('{}/{}').format(instance.title, filename)
    
    name = models.CharField(max_length=100, verbose_name="Название", null=True, blank=False)
    short_description = models.CharField(max_length=300, verbose_name="Краткое описание", null=True, blank=False, help_text="Будет выводиться на главной странице. Максимум - 300 символов.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="categ_products", verbose_name="Категория", help_text="Группа товара, по которой будет фильтроваться их список.")
    amount = models.IntegerField(verbose_name="Кол-во", default=0, help_text="Количество товара на складе") # editable = False
    male_female = models.CharField(max_length=10, choices=SEX, default="U", verbose_name='М/Ж?')
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Цена", default=0.0, blank=False) 
    description = models.TextField(max_length=1000, verbose_name="Длинное описание товара. Будет выводиться на его личной странице.", null=True, blank=True)
    is_limited = models.BooleanField(verbose_name="Лимитированый?", default=False)
    archived = models.BooleanField(verbose_name="Архивирован?", default=False)
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")

class Photo(models.Model):
    """ Фотография товара """

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"

    def __str__(self) -> str:
        return f'{self.photo.url}<--[{self.product.name}]'

    def directory_path(instance, filename:str):
        return f"product_id_{instance.product.pk}/{filename}"
    
    # def save(self, *args, **kwargs):
        #from PIL import Image
        # super(Photo, self).save(*args, **kwargs)
        # img = Image.open(self.photo.path)
        # if img.height > 1125 or img.width > 1125:
        #     img.thumbnail((1125,1125))
        # img.save(self.photo.path,quality=70,optimize=True)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos', help_text="Нужно выбрать товар, которому соответствует данная картинка.")
    photo = models.ImageField(verbose_name="Изображение", upload_to=directory_path) # 

class Promocode(models.Model):
    """ Промокод на скидку """
    class Meta:
        verbose_name = "Промокод на скидку"
        verbose_name_plural = "Промокоды на скидку"

    @staticmethod
    def does_have_promocode(user):
        """ Дичь !!!! """
        try:
            user.promocode
            return True
        except:
            return False

    def __str__(self):
        return f'№{self.pk} "{self.code}"'
    
    def str_v2(self):
        return f'"{self.code}"'
    
    def generate_code(self):
        """ Генерирует строку промокода. """
        CODE_LEN = 4 # 1.5 millions variations
        code = ''
        signs = string.ascii_uppercase + '0123456789'
        for l in range(CODE_LEN):
            code += choice(signs)
        return code
    
    def is_valid(self): # поменять на is_valid_date() или что-то такое.
        """ Не истек ли срок годности промокода. """
        return (self.end_date - datetime.datetime.now(datetime.timezone.utc)).days > 0
    
    def days_left(self):
        """ Выводит кол-во оставшихся дней. """
        return max((self.end_date - datetime.datetime.now(datetime.timezone.utc)).days, 0)

    def save(self, *args, **kwargs):
        if not self.pk: # сработает в случае создания записи
            now = datetime.datetime.now()
            now_plus_month = now.timestamp() + ( 30 * 24 * 60 * 60 )
            new_now = datetime.datetime.fromtimestamp(now_plus_month) # переводим из секунд в объект datetime
            self.end_date = new_now
            self.code = self.generate_code()
        super(Promocode, self).save(*args, **kwargs)
        
    code = models.CharField(max_length=10, verbose_name="Код промокода", null=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Чей промокод", related_name='promocode', null=True)
    percent = models.IntegerField(verbose_name="Процент скидки (%)", default=10)
    add_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, editable=False)
    


    


