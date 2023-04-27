from django.contrib import admin
from .models import Promocode, Product, Category, Photo

class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'code', 'user', 'add_date', 'end_date', 'days_left')

class PhotoAdmin(admin.StackedInline):
    model = Photo
    #list_display = ('pk', 'photo', 'product')
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'male_female', 'price', 'is_limited', 'archived', 'add_date')
    list_filter = [ 'category', 'is_limited', 'archived', 'male_female']
    ordering = ['add_date',]
    search_fields = ['pk', 'name', 'add_date']
    inlines = [PhotoAdmin]
    class Meta:
        model = Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)



admin.site.register(Product, ProductAdmin)
admin.site.register(Promocode, PromocodeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo)

# Register your models here.
