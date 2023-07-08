from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from orders.models import Order
from yookassa import Configuration, Payment
#import var_dump as var_dump
import random

@csrf_exempt
def status(request):
    """ Отлавливает сообщения от юкассы с обновлениями статусов заказов - оплата"""

    print("--------------Данные от Yookassa--------------")
    print(json.loads(request.body))
    print('----------------------------------------------')

    py_data = json.loads(request.body) # преобразуем в формат python

    order_pk = py_data['object']['metadata']['orderNumber'] # номер заказа в базе данных через metadata
    event = py_data['event'] 
    
    paid_order = Order.objects.filter(pk=order_pk).first()
    if event == 'payment.succeeded': # подтверждение оплаты 
        print(f"Пришла оплата на заказ {order_pk}")
        if paid_order is not None: # если такой заказ существует
            paid_order.paid = True
            paid_order.status = 'OTW' 
            paid_order.payment_status = 'ON'
            paid_order.save()
        else:
            print(f'Заказа под номером {order_pk} не существует!!!')
            raise ValueError
    elif event == 'payment.canceled':
        paid_order.paid = False
        paid_order.payment_status = 'NA'
        paid_order.status = 'RTP'
        print(f"Пришла отмена оплаты на заказ {order_pk}")
    else:
        print("Неизвестный тип сообщения от юкассы!")
    return HttpResponse('good')


""" {
   "type":"notification",
   "event":"payment.succeeded",
   "object":{
      "id":"2c3685b4-000f-5000-8000-125c39467cd9",
      "status":"succeeded",
      "amount":{
         "value":"240000.00",
         "currency":"RUB"
      },
      "income_amount":{
         "value":"231600.00",
         "currency":"RUB"
      },
      "description":"Заказ №66",
      "recipient":{
         "account_id":"223675",
         "gateway_id":"2094170"
      },
      "payment_method":{
         "type":"bank_card",
         "id":"2c3685b4-000f-5000-8000-125c39467cd9",
         "saved":false,
         "title":"Bank card *4477",
         "card":{
            "first6":"555555",
            "last4":"4477",
            "expiry_year":"2024",
            "expiry_month":"11",
            "card_type":"MasterCard",
            "issuer_country":"US"
         }
      },
      "captured_at":"2023-07-04T19:25:13.535Z",
      "created_at":"2023-07-04T19:24:36.191Z",
      "test":true,
      "refunded_amount":{
         "value":"0.00",
         "currency":"RUB"
      },
      "paid":true,
      "refundable":true,
      "metadata":{
         "orderNumber":"66"
      },
      "authorization_details":{
         "rrn":"316196843308140",
         "auth_code":"803511",
         "three_d_secure":{
            "applied":true,
            "protocol":"v1",
            "method_completed":false,
            "challenge_completed":true
         }
      }
   }
}"""
