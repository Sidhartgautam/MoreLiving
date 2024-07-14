from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'message', 'created_at', 'is_read')
    list_filter = ('hotel', 'is_read', 'created_at')
    search_fields = ('hotel__hotel_name', 'message')
    readonly_fields = ('created_at',)

    def hotel(self, obj):
        return obj.hotel.hotel_name
    hotel.admin_order_field = 'hotel__hotel_name'  # Allows column order sorting
    hotel.short_description = 'Hotel'  # Renames column head
