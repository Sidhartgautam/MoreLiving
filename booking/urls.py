from django.urls import path
from .views import BookingCreateView, BookingListView,BookingCancelView

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<uuid:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]
