from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display=("name","description","price","image","category","get_suppliers")
    def get_suppliers(self, obj):
        return ", ".join([supplier.name for supplier in obj.suppliers.all()])
    get_suppliers.short_description = 'Suppliers'


admin.site.register(Product,ProductAdmin)
