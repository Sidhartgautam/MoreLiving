# rooms/urls.py
from django.urls import path
from .views import (
    RoomView, RoomListView,RoomDetailsView,
    RoomTypeCreate, RoomTypeListView,
    RoomImageCreate, RoomImageListView,
    RoomAmenitiesCreate, RoomAmenitiesListView
)

urlpatterns = [
    # Room URLs
    path('rooms/list/<uuid:hotel_id>/', RoomListView.as_view(), name='room-list'),
    path('rooms/<uuid:hotel_id>/<uuid:room_id>/details/', RoomDetailsView.as_view(), name='room-details'),
    path('rooms/create/', RoomView.as_view(), name='room-create'),


    # RoomType URLs
    path('room-types/create/', RoomTypeCreate.as_view(), name='roomtype-create'),
    path('room-types/list/', RoomTypeListView.as_view(), name='roomtype-list'),

    # RoomImage URLs
    path('room-images/create/', RoomImageCreate.as_view(), name='roomimage-create'),
    path('room-images/list/', RoomImageListView.as_view(), name='roomimage-list'),

    # RoomAmenities URLs
    path('room-amenities/create/', RoomAmenitiesCreate.as_view(), name='roomamenities-create'),
    path('room-amenities/list/', RoomAmenitiesListView.as_view(), name='roomamenities-list'),
]


