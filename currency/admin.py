from django.contrib import admin

from .models import Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'currency_code', 'currency_symbol')
    list_filter = ('currency_name', 'currency_code', 'currency_symbol')
    search_fields = ('currency_name', 'currency_code', 'currency_symbol')