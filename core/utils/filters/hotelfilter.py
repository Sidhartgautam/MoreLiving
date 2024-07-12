# hotels/filters.py

import django_filters
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
