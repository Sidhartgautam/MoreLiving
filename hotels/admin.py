# hotel/admin.py

from django.contrib import admin
from .models import Hotel, HotelType

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ( 'id','hotel_name', 'hotel_contact', 'country', 'city', 'state','user')
    fieldsets = (
        (None, {'fields': ('hotel_name', 'hotel_contact', 'hotel_type', 'country', 'address', 'city', 'state', 'lng', 'lat')}),
        )
    search_fields = ('hotel_name', 'city', 'state')
    list_filter = ('country', 'city', 'state')
    ordering = ('hotel_name',)
    filter_horizontal = ('hotel_type',)

@admin.register(HotelType)
class HotelTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)
    search_fields = ('type_name',)
    ordering = ('type_name',)
