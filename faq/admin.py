from django.contrib import admin

# Register your models here.
from .models import HotelFAQ, MoreLivingFAQ

admin.site.register(HotelFAQ)
admin.site.register(MoreLivingFAQ)
