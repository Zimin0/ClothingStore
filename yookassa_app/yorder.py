# from yookassa import Configuration, Payment
# from django.conf import settings

# Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)

# def create_yookassa_order(order):
#     """ Создает заказ yookassa на основе модели Order. """
#     items = []
#     for item in order.items.all():
#         items.append({
#             "description": item.product.name,
#             "quantity": str(item.quantity),
#             "amount": {
#                 "value": str(item.get_cost()),
#                 "currency": "RUB"
#             },
#             "vat_code": "1",
#             "payment_mode": "full_payment",
#             "payment_subject": "commodity",
#         })

#     payment = Payment.create({
#         "amount": {
#             "value": str(order.get_total_cost()),
#             "currency": "RUB"
#         },
#         "confirmation": {
#             "type": "redirect",
#             "return_url": settings.YOOKASSA_RETURN_URL
#         },
#         "capture": True,
#         "description": f"Заказ №{order.id}",
#         "metadata": {
#             'order_id': str(order.id)
#         },
#         "receipt": {
#             "customer": {
#                 "full_name": f"{order.first_name} {order.last_name}",
#                 "email": order.email,
#                 "phone": order.phone,
#             },
#             "items":
