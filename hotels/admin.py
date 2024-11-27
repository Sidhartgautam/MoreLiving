# hotel/admin.py

from django.contrib import admin
from .models import Hotel, HotelType, HotelFacility, HotelImage,PropertyType

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ( 'id','hotel_name', 'hotel_contact', 'country', 'city', 'state','user')
    fieldsets = (
        (None, {'fields': ('user','hotel_name', 'hotel_contact', 'hotel_type','hotel_email','property_type','country', 'address', 'city', 'state', 'lng', 'lat')}),
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


@admin.register(HotelFacility)
class HotelFacilityAdmin(admin.ModelAdmin):
    list_display = ('facility_name', 'hotel')
    search_fields = ('facility_name', 'hotel__hotel_name')
    ordering = ('facility_name',)

@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'image')
    search_fields = ('hotel__hotel_name',)

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)
    search_fields = ('type_name',)
    ordering = ('type_name',)


