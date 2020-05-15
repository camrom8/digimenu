from django.contrib import admin

# Register your models here.
from menus import models

admin.site.register(models.Menu)
admin.site.register(models.Item)
admin.site.register(models.Establishment)
admin.site.register(models.Category)
admin.site.register(models.Price)