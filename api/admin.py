from django.contrib import admin

from api.models import Truck


@admin.register(Truck, site=admin.site)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('name', 'handle')
