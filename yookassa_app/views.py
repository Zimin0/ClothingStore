from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def main(request):
    print("--------------Данные от Yookassa--------------")
    print(json.loads(request.body))
    print('----------------------------------------------')
    return HttpResponse('good')

@csrf_exempt
def create(request):
    from yookassa import Configuration, Payment
    #import var_dump as var_dump
    import random

    Configuration.configure('223675', 'test_TTAs0tK1cXQttfoCwGx6R2vYj_YUYuxoIJW2YdJB9ck')

    val = random.randint(1000,5000)

    res = Payment.create(
        {
            "amount": {
                "value": val,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://merchant-site.ru/return_url"
            },
            "capture": True,
            "description": f"Заказ №{val}",
            "metadata": {
                'orderNumber': f'{val}'
            },
            "receipt": {
                "customer": {
                    "full_name": "Ivanovg Ivan Ivanovich",
                    "email": "email@email.ru",
                    "phone": "79211232145",
                    "inn": "6354321814"
                },
                "items": [
                    {
                        "description": "Переносное зарядное устройство Хувей",
                        "quantity": "1.00",
                        "amount": {
                            "value": val,
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
                    },
                ]
            }
        }
    )

    #var_dump.var_dump(res)
    #var_dump.var_dump(res)
    return HttpResponse(f"<h1>Заказ №{val} создан! </h1> <br> <a>{res.confirmation.confirmation_url}</a>")