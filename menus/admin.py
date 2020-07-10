from django.contrib import admin
import pprint
from django.contrib.sessions.models import Session
# Register your models here.
from menus import models

admin.site.register(models.Menu)
admin.site.register(models.Establishment)
admin.site.register(models.ProductInCart)
admin.site.register(models.Quantity)


@admin.register(models.AddsOn)
class AddsOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_str', 'price')
    list_editable = ('price_str', 'price')


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('item', 'size', 'price_str', 'price')
    list_editable = ('price_str', 'price')


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'menu', 'photo')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'position')


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')

    _session_data.allow_tags = True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
    date_hierarchy = 'expire_date'


admin.site.register(Session, SessionAdmin)
