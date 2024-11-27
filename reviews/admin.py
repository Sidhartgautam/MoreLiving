from django.contrib import admin

from .models import HotelReview, GuestReview

# Register your models here.

admin.site.register(HotelReview)
admin.site.register(GuestReview)
