from django.contrib import admin
from discount.models import Discount
from pages.models import Product

class ProductInline(admin.StackedInline):
    model = Product

class DiscountAdmin(admin.ModelAdmin):
    class Meta:
        model = Discount

    list_display = ('name', 'is_expired', 'percent', 'start_date', 'end_date')
    ordering = ['start_date',]
    # inlines = [ProductInline]

admin.site.register(Discount, DiscountAdmin)