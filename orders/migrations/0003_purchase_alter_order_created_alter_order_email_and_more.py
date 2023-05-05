# Generated by Django 4.1.6 on 2023-05-04 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_city_alter_order_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Запрос на покупку',
                'verbose_name_plural': 'Запросы на покупки',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Электронный адрес'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Ополачен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='postal_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Почтовый индекс'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлен'),
        ),
    ]
