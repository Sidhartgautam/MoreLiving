from django.urls import path
from .views import HotelFAQView,WebsiteFAQView,HotelFAQCreateView,WebsiteFAQCreateView

urlpatterns = [
    path('hotel-faqs/', HotelFAQView.as_view(), name='hotel-faq-list'),
    path('hotel-faqs/create/', HotelFAQCreateView.as_view(), name='hotel-faq-create'),
    path('website-faqs/', WebsiteFAQView.as_view(), name='website-faq-list'),
    path('website-faqs/create/', WebsiteFAQCreateView.as_view(), name='website-faq-create'),
]
    