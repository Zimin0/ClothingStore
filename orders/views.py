from django.shortcuts import render, HttpResponse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart    
from django.contrib import messages
from pages.models import Promocode 
import decimal
from yookassa_app.yorder import create_yookassa_payment

import logging
logger = logging.getLogger(__name__)

def order_create(request):
    """ Создает заказ модели Order + юкасса"""
    cart = Cart(request) # достаем объект корзины из сессии
    curr_user = request.user

    if request.method == 'POST':
        form = OrderCreateForm(request.POST) 
        if form.is_valid():
            order = form.save()
            promo = request.POST['promocode']
            total_price = cart.get_total_price() # чистая суммарная цена всех товаров в корзине
            if promo != '' and not(cart.is_promocode_applied): # если промокод введен пользователем
                ### сохранить чек (или сохранится в юкассе)
                promocode_used = Promocode.objects.get(code=promo) # получаем введенный промокод
                
                order.promocode_used = promocode_used # Добавляем в объект заказа использованный промокод

                if request.user.is_anonymous: # временно 
                    return HttpResponse("<h1> Пока не понятно, что делать, если пользователь ввел промокод, но он не зарегестрирован или не вошел в аккаунт...</h1>")
                
                total_price, points_to_promo_owner = order.process_the_order(request.user, total_price, promocode_used.percent, promocode_used.user, promocode_used.pk)
                promocode_used.user.profile.points += decimal.Decimal(points_to_promo_owner)
                promocode_used.user.profile.save()
                cart.add_promo() # Добавляет метку к корзине, что промокод уже применен.

                print("------------------Обработка-заказа------------------")
                print(total_price, points_to_promo_owner)
                print("----------------------------------------------------")

            order.total_price = total_price 
            order.save()
            for item in cart: # создаем в БД объекты товаров, привязанных к Order`у
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])            
            cart.clear() # очистка корзины
            host = request.META['HTTP_HOST'] # получение хоста 
            print("ХОСТ =", host)
            yookassa_order = create_yookassa_payment(order, host) 

            return render(request, 'orders/order/ready_to_pay.html',
                          {'order': order,
                           'sum': cart.get_total_price(),
                           'pay_link': yookassa_order.confirmation.confirmation_url
                           })
        else:
            # эта строчка ниже нужна, чтобы при валидации формы в forms.py отобразились ошибки.
            return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
        
    elif request.method == 'GET': # Если пойман метод GET
        if cart.is_not_empty: # если сумма в корзине больше нуля
            if request.user.is_anonymous: # Если заказ оформляет незарегестрировавшийся пользователь
                form = OrderCreateForm() # Пустая форма
            else:
                form = OrderCreateForm(initial={ # передаем в форме значения, введенные в личном кабинете. 
                    'first_name': curr_user.first_name,
                    'last_name': curr_user.last_name,
                    'email': curr_user.email,
                    'phone' : curr_user.profile.phone, 
                    'address' : curr_user.profile.address
                })
            return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
        else: # Если корзина пуста
            messages.error(request, 'Корзина пуста!')
            return render(request, 'cart/detail.html', {'cart': cart})
        
    else:
        return HttpResponse("<h1> Неизвестный метод отправки! </h1>")