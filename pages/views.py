from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from .models import Promocode, Product
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddProductForm 

import logging
logger = logging.getLogger(__name__)


def main(request):
    """ Каталог главной страницы"""
    context = {}
    context['user'] = request.user
    context['products'] = Product.objects.all()[:4]
    return render(request, "pages/main.html", context)

@login_required
def promocode(request):
    """ Оформление промокода """
    context = {}
    context['promo_already_exists'] = Promocode.does_have_promocode(request.user) # проверка на то, что промокод уже существует 

    if request.method == 'POST':
        logger.warning("Перехвачен метод POST в promocode.url")
        if request.POST['makepromo'] == 'yes':
            Promocode.objects.create(user=request.user)
            logger.warning("Новый промод создан.")

    context['user'] = request.user
    context['promocode'] = request.user.promocode
    return render(request, "pages/promocode.html", context)

@login_required
def profile(request):
    """Личный кабинет """
    context = {}
    try:
        context['promocode'] = request.user.promocode
    except: 
        context['promocode'] = "У вас пока его нет!"
    return render(request, "pages/profile.html", context)

def ex_product(request, prod_id):
    """ Страница продукта """
    product = get_object_or_404(Product, id=prod_id)
    cart_product_form = CartAddProductForm()
    context = {'product': product,
               'cart_product_form': cart_product_form}
    context['product'] = Product.objects.get(id=prod_id)
    return render(request, 'pages/product.html', context)

def limited(request):
    context = {}
    context['user'] = request.user
    context['products'] = Product.objects.filter(is_limited=True)[:4]
    return render(request, "pages/limited.html", context)

def brand_creation(request):
    return render(request, "pages/brand_creation.html") 

def contacts(request):
    return render(request, "pages/contacts.html") 