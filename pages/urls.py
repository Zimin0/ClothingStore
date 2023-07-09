from django.urls import path
from .views import promocode, profile, main, ex_product, limited, brand_creation, contacts, my_orders, men, women

app_name = 'pages'

urlpatterns = [
    path('', main, name='main'),
    path('promocode/', promocode, name='promocode'),
    path('profile/', profile, name='profile'),
    path('<int:prod_id>/', ex_product, name='ex_product'),
    path('limited/', limited, name='limited'),
    path('brand_creation/', brand_creation, name='brand_creation'),
    path('contacts/', contacts, name='contacts'),
    path('my_orders/', my_orders, name='my_orders'),
    path('men/', men, name='men'),
    path('women/', women, name='women'),
]
