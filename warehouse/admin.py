from django.contrib import admin

from warehouse.models import Supply, SupplyItem


class SupplyItemAdmin(admin.StackedInline):
    model = SupplyItem

class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id','add_date')
    #list_filter = [ 'category', 'is_limited', 'archived', 'male_female']
    ordering = ['add_date',]
    #search_fields = ['pk', 'name', 'add_date']
    inlines = [SupplyItemAdmin]
    class Meta:
        model = Supply


admin.site.register(Supply, SupplyAdmin)
admin.site.register(SupplyItem)