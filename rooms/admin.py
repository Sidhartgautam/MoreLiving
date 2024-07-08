# rooms/admin.py

from django.contrib import admin
from .models import Room, RoomType, RoomStatus, RoomImage, RoomAmenities

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name',)
    search_fields = ('type_name',)
    ordering = ('type_name',)

@admin.register(RoomStatus)
class RoomStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_status',)
    search_fields = ('room_status',)
    ordering = ('room_status',)

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_number', 'room_status', 'room_type', 'hotel', 'room_price', 'floor')
    search_fields = ('room_number', 'hotel__hotel_name', 'room_type__type_name', 'room_status__status')
    list_filter = ('hotel', 'room_status', 'room_type')
    inlines = [RoomImageInline]

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'image',)
    search_fields = ('room__room_number',)
    list_filter = ('room',)

@admin.register(RoomAmenities)
class RoomAmenitiesAdmin(admin.ModelAdmin):
    list_display = ('amenity_name',)
    search_fields = ('amenity_name',)
    ordering = ('amenity_name',)
