from django.urls import path
from .views import BookingCreateAPIView, BookingListView,BookingCancelView

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/<uuid:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]
