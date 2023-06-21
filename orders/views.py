from django.shortcuts import render, HttpResponse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart    
from django.contrib import messages
from pages.models import Promocode 

import logging
logger = logging.getLogger(__name__)

def order_create(request):
    cart = Cart(request) # достаем объект корзины из сессии
    curr_user = request.user

    if request.method == 'POST':
        form = OrderCreateForm(request.POST) 
        if form.is_valid():
            # Начислить скидку 10 процентов
            order = form.save()
            print("------------------Обработка-заказа------------------")
            print(order.process_the_order(request.user))
            print("----------------------------------------------------")
            promo = request.POST['promocode']
            if promo != '' and not(cart.is_promocode_applied): # если промокод введен пользователем
                order.promocode_used = Promocode.objects.get(code=promo) 
                curr_user.profile.linked_to_promer = Promocode.objects.get(code=promo).user
                curr_user.save() # возможно, стоит удалить
                cart.add_promo() # Добавляет метку, что промокод уже применен.
                order.save()
                
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear() # очистка корзины
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
    