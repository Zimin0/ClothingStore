#from django.test import TestCase
#
# Create your tests here.
#from django.contrib.auth.models import User
#print(User.objects.get(username="admin").promocode)
#profile = Profile.objects.create(user=User.objects.get(username="admin"))


from pages.models import Product, Category, Photo
from django.core.management.base import BaseCommand
import random



def load_Categories():
    for n in range(1,10):
        Category.objects.create(name=f'Категория{n}')

def load_Products():
    all_cats = Category.objects.all()
    for i in all_cats:
        for j in range(1,51):
            Product.objects.create(
                name=f"Товар{j}",
                short_description=f'Краткое описание товара {j}, содержит немного информации для презентации товара на главной странице.',
                category= random.choice(all_cats),
                male_female=random.choice(Product.SEX)[0],
                price=random.uniform(1000.0, 150000.0),
                description="Полное описание товара +"*20,
            )
