from django.urls import path
from .views import (
    RoomView, RoomListView,
    RoomTypeCreate, RoomTypeListView,
    RoomStatusCreate, RoomStatusListView,
    RoomImageCreate, RoomImageListView,
    RoomAmenitiesCreate, RoomAmenitiesListView
)

urlpatterns = [
    # Room URLs
    path('rooms/<uuid:hotel_id>/list/', RoomListView.as_view(), name='room-list'),
    path('rooms/create/', RoomView.as_view(), name='room-create'),

    # RoomType URLs
    path('room-types/list/', RoomTypeListView.as_view(), name='roomtype-list'),
    path('room-types/create/', RoomTypeCreate.as_view(), name='roomtype-create'),

    # RoomStatus URLs
    path('room-statuses/', RoomStatusListView.as_view(), name='roomstatus-list'),
    path('room-statuses/create/', RoomStatusCreate.as_view(), name='roomstatus-create'),

    # RoomImage URLs
    path('room-images/', RoomImageListView.as_view(), name='roomimage-list'),
    path('room-images/create/', RoomImageCreate.as_view(), name='roomimage-create'),

    # RoomAmenities URLs
    path('room-amenities/', RoomAmenitiesListView.as_view(), name='roomamenities-list'),
    path('room-amenities/create/', RoomAmenitiesCreate.as_view(), name='roomamenities-create'),
]
