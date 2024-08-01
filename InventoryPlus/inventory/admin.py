from django.contrib import admin
from .models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    list_display= ("product","quantity", "status","create_date") # display this attribute in admin dashboard
    
admin.site.register(Inventory,InventoryAdmin)
