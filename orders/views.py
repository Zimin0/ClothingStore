from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart    
from django.contrib import messages

def order_create(request):
    cart = Cart(request) # достаем объект корзины из сессии
    curr_user = request.user
    if request.method == 'POST':
        form = OrderCreateForm(data=request.POST) # ???
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
        
    else:
        if cart.get_total_price() > 0: # если сумма в корзине больше нуля
            form = OrderCreateForm(initial={
                'first_name': curr_user.first_name,
                'last_name': curr_user.last_name,
                'email': curr_user.email,
                'phone' : curr_user.profile.phone, 
                'address' : curr_user.profile.address
            })
            return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})
        else: # Если корзина пуста
            messages.error(request, 'Корзина пуста!')
            return render(request, 'cart/detail.html', {'cart': cart})
    