# hotels/filters.py

import django_filters
from django_filters import rest_framework as filters
from hotels.models import Hotel
from rooms.models import Room
from django.db.models import Q
from hotels.models import Hotel, HotelType, HotelFacility, HotelImage

class HotelFilter(django_filters.FilterSet):
    min_lat = django_filters.NumberFilter(field_name='lat', lookup_expr='gte')
    max_lat = django_filters.NumberFilter(field_name='lat', lookup_expr='lte')
    min_lng = django_filters.NumberFilter(field_name='lng', lookup_expr='gte')
    max_lng = django_filters.NumberFilter(field_name='lng', lookup_expr='lte')
    hotel_name = django_filters.CharFilter(field_name='hotel_name', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    state = django_filters.CharFilter(field_name='state', lookup_expr='icontains')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('hotel_name', 'hotel_name'),
            ('city', 'city'),
            ('state', 'state'),
            ('lng', 'lng'),
            ('lat', 'lat'),
        )
    )

    class Meta:
        model = Hotel
        fields = ['min_lat', 'max_lat', 'min_lng', 'max_lng', 'hotel_name', 'city', 'state']

class HotelTypeFilter(django_filters.FilterSet):
    type_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = HotelType
        fields = ['type_name']

class HotelImageFilter(django_filters.FilterSet):
    image = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = HotelImage
        fields = ['image']

class HotelFacilityFilter(django_filters.FilterSet):
    facility_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = HotelFacility
        fields = ['facility_name']

class HotelSearchFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="city__city_name", lookup_expr="icontains")
    country = filters.CharFilter(field_name="country__name", lookup_expr="icontains")
    check_in = filters.DateFilter(method="filter_availability")
    check_out = filters.DateFilter(method="filter_availability")
    guests = filters.NumberFilter(method="filter_room_capacity")
    min_price = filters.NumberFilter(field_name="rooms__room_price", lookup_expr="gte", method="filter_price_range")
    max_price = filters.NumberFilter(field_name="rooms__room_price", lookup_expr="lte", method="filter_price_range")

    class Meta:
        model = Hotel
        fields = ['city', 'country', 'check_in', 'check_out', 'guests', 'min_price', 'max_price']

    def filter_availability(self, queryset, name, value):
        check_in = self.data.get('check_in')
        check_out = self.data.get('check_out')
        if check_in and check_out:
            # Filter hotels that have rooms available for the given dates
            queryset = queryset.filter(
                Q(rooms__bookings__check_out__lte=check_in) |
                Q(rooms__bookings__check_in__gte=check_out) |
                Q(rooms__bookings__isnull=True)
            ).distinct()
        return queryset

    def filter_room_capacity(self, queryset, name, value):
        guests = self.data.get('guests')
        if guests:
            # Filter hotels with rooms that can accommodate the guest count
            queryset = queryset.filter(rooms__max_guests__gte=guests).distinct()
        return queryset

    def filter_price_range(self, queryset, name, value):
        min_price = self.data.get('min_price')
        max_price = self.data.get('max_price')
        if min_price or max_price:
            # Filter hotels with rooms within the price range
            queryset = queryset.filter(
                Q(rooms__room_price__gte=min_price) if min_price else Q(),
                Q(rooms__room_price__lte=max_price) if max_price else Q(),
            ).distinct()
        return queryset
