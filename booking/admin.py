from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'room', 'check_in', 'check_out', 'status', 'created_at', 'updated_at')
    search_fields = ('id', 'user__username', 'hotel__hotel_name', 'room__room_number', 'status__status')
    readonly_fields = ('created_at', 'updated_at')
