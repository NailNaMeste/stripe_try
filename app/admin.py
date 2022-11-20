from django.contrib import admin

# Register your models here.

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass