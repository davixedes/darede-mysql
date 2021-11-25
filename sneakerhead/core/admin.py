from django.contrib import admin
from core.models import *

# class ProdutosAdmin(admin.ModelAdmin):
#     fields = ['name', 'last_name', 'age', 'salary']
#     list_display = ['name', 'last_name', 'age', 'salary']
#     list_filter = ['name', 'last_name', 'age', 'salary']
#     search_fields = ['last_name', 'age']
# 
# admin.site.register(Produtos, ProdutosAdmin)

class InventoryAdmin(admin.ModelAdmin):
    fields = ['product', 'amount']
    list_display = ['product', 'amount']

admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Demand)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Delivery)
admin.site.register(Card)
