from django.shortcuts import render, HttpResponse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart    
from django.contrib import messages
from pages.models import Promocode 
import decimal

import logging
logger = logging.getLogger(__name__)

def order_create(request):
    print(request.user.profile.linked_to_promer is not None)
    cart = Cart(request) # достаем объект корзины из сессии
    curr_user = request.user

    if request.method == 'POST':
        form = OrderCreateForm(request.POST) 
        if form.is_valid():
            order = form.save()
            promo = request.POST['promocode']
            if promo != '' and not(cart.is_promocode_applied): # если промокод введен пользователем
                ### создать объект payment yookassa
                ### сохранить чек (или сохранится в юкассе)
                ### добавить редирект на оплату
                promocode_used = Promocode.objects.get(code=promo) # получаем введенный промокод
                total_price = cart.get_total_price() # чистая суммарная цена всех товаров в корзине
                order.promocode_used = promocode_used # Добавляем в объект заказа использованный промокод
                total_price, points_to_promo_owner = order.process_the_order(request.user, total_price, promocode_used.percent, promocode_used.user, promocode_used.pk)
                order.total_price = total_price 
                promocode_used.user.profile.points += decimal.Decimal(points_to_promo_owner)
                promocode_used.user.profile.save()
                print("------------------Обработка-заказа------------------")
                print(total_price, points_to_promo_owner)
                print("----------------------------------------------------")

                #### Загнать в отдельную функцию в классе Order ###
                
                ###################################################
                cart.add_promo() # Добавляет метку, что промокод уже применен.
                order.save()
            
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            
            cart.clear() # очистка корзины

            #### Загнать в отдельную функцию в классе Order ###
            curr_user.profile.bought_already = True  
            curr_user.save() # возможно, стоит удалить
            print(f'Для {curr_user} отмечено, что он покупал ранее.')  

            ###################################################
            return render(request, 'orders/order/created.html',
                          {'order': order,
                           'sum': cart.get_total_price()})
        else:
            # эта строчка ниже нужна, чтобы при валидации формы в forms.py отобразились ошибки.
            return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
    else: # Если пойман метод GET
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
    