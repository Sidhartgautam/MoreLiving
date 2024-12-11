# hotels/filters.py
from django.db import models
import django_filters
from django_filters import rest_framework as filters
from hotels.models import Hotel
from rooms.models import Room
from booking.models import Booking
from django.db.models import Q,Count
from django.utils.dateparse import parse_datetime
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
    check_in = filters.DateTimeFilter(method="filter_availability")  
    check_out = filters.DateTimeFilter(method="filter_availability") 
    adults = filters.NumberFilter(method="filter_room_capacity")
    children = filters.NumberFilter(method="filter_room_capacity")
    rooms= filters.NumberFilter(method="filter_number_of_rooms")
    min_price = filters.NumberFilter(field_name="rooms__room_price", lookup_expr="gte", method="filter_price_range")
    max_price = filters.NumberFilter(field_name="rooms__room_price", lookup_expr="lte", method="filter_price_range")

    class Meta:
        model = Hotel
        fields = ['city', 'country', 'check_in', 'check_out', 'adults', 'children', 'min_price', 'max_price']

    def filter_availability(self, queryset, name, value):
        check_in = self.data.get('check_in')
        check_out = self.data.get('check_out')

        if check_in and check_out:
            try:
                # Parse check-in and check-out dates
                check_in_date = parse_datetime(check_in)
                check_out_date = parse_datetime(check_out)

                # Fetch unavailable room IDs
                unavailable_room_ids = Booking.objects.filter(
                    status="confirmed",
                    check_in__lt=check_out_date,
                    check_out__gt=check_in_date
                ).values_list('room_id', flat=True)
                queryset = queryset.filter(rooms__id__in=unavailable_room_ids).distinct()

                print("Unavailable Room IDs:", list(unavailable_room_ids))
                print("Filtered Hotels:", queryset)  # Debugging
            except ValueError as e:
                print("Error parsing dates:", e)  # Handle invalid dates gracefully
        return queryset
    
    def filter_room_capacity(self, queryset, name, value):
        adults = int(self.data.get('adults', 0))
        children = int(self.data.get('children', 0))
        total_guests = adults + children

        if total_guests:
            # Filter hotels with rooms that can accommodate the total guest count
            queryset = queryset.filter(rooms__max_guests__gte=total_guests).distinct()
        return queryset
    
    def filter_number_of_rooms(self, queryset, name, value):
        check_in = self.data.get('check_in')
        check_out = self.data.get('check_out')
        rooms = int(value)

        if not rooms:
            return queryset

        if check_in and check_out:
            try:
                check_in_date = parse_datetime(check_in)
                check_out_date = parse_datetime(check_out)

                # Fetch unavailable room IDs
                unavailable_room_ids = Booking.objects.filter(
                    status="confirmed",
                    check_in__lt=check_out_date,
                    check_out__gt=check_in_date
                ).values_list('room_id', flat=True)

                # Annotate hotels with available room counts
                queryset = queryset.annotate(
                    available_rooms_count=Count(
                        'rooms',
                        filter=~Q(rooms__id__in=unavailable_room_ids)
                    )
                ).filter(available_rooms_count__gte=rooms)
            except ValueError as e:
                print("Error parsing dates:", e)
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
