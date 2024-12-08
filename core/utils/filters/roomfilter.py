# rooms/filters.py

import django_filters
from rooms.models import Room, RoomType, RoomImage, RoomAmenities

class RoomFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='room_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='room_price', lookup_expr='lte')
    room_type = django_filters.CharFilter(field_name='room_type__type_name', lookup_expr='icontains')
    room_status = django_filters.CharFilter(field_name='room_status__status', lookup_expr='icontains')
    hotel = django_filters.CharFilter(field_name='hotel__hotel_name', lookup_expr='icontains')

    class Meta:
        model = Room
        fields = ['min_price', 'max_price', 'room_type', 'room_status', 'hotel']

class RoomTypeFilter(django_filters.FilterSet):
    type_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = RoomType
        fields = ['type_name']


class RoomImageFilter(django_filters.FilterSet):
    room = django_filters.CharFilter(field_name='room__room_number', lookup_expr='icontains')

    class Meta:
        model = RoomImage
        fields = ['room']

class RoomAmenitiesFilter(django_filters.FilterSet):
    amenity_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = RoomAmenities
        fields = ['amenity_name']
