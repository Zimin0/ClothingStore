from yookassa import Configuration, Payment
from orders.models import OrderItem
import var_dump
from decimal import Decimal

def create_yookassa_payment(order_obj, host):
    """ 
    Создает запрос на оплату Юкассы. 
    Принимает объект модели Order.
    """

    Configuration.configure('223675', 'test_TTAs0tK1cXQttfoCwGx6R2vYj_YUYuxoIJW2YdJB9ck')
    data = {
            "amount": {
                "value": order_obj.total_price,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": 'http://' + str(host)
            },
            "capture": True,
            "description": f"Заказ №{order_obj.pk}",
            "metadata": {
                'orderNumber': f'{order_obj.pk}'
            },
            "receipt": {
                "customer": {
                    "full_name": f'{order_obj.last_name}{order_obj.first_name}',
                    "email": order_obj.email,
                    "phone": order_obj.phone,
                    "inn": "no inn" # Его обязательно нужно передавать???
                },
                "items": [] # сюда по отдельности будут добавляться товары, присутствующие в заказе
            }
        }
    
    # Добавление отдельных товаров в заказ Юкассы
    for item in OrderItem.objects.filter(order=order_obj):
        item_data = {
                        "description": item.product.short_description,
                        "quantity": str(Decimal(item.quantity)),
                        "amount": {
                            "value": item.price,
                            "currency": "RUB"
                        },
                    "vat_code": "2",
                    "payment_mode": "full_payment",
                    "payment_subject": "commodity",
                    "country_of_origin_code": "CN",
                    "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                    "customs_declaration_number": "10714040/140917/0090376",
                    "excise": "20.00",
                    "supplier": {
                        "name": "string",
                        "phone": "string",
                        "inn": "string"
                        }
                    }
        data['receipt']['items'].append(item_data)

    #var_dump.var_dump(pmnt)
    return Payment.create(data)