from pages.models import Product, Category, Photo
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Эта команда предназначена для вставки издателя, книги, магазина в базу данных.
    Добавляет 5 издателей, 100 книг, 10 магазинов.
    """
    def handle(self, *args, **options):
        def load_Categories():
            for n in range(1,2):
                Category.objects.create(name=f'Категория{n}')
        load_Categories()

