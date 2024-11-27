import django_filters
from reviews.models import HotelReview,GuestReview

class HotelReviewFilter(django_filters.FilterSet):
    class Meta:
        model =HotelReview
        fields =[
            'hotel',
            'user',
            'comment',
            'rating',
        ]

class GuestReviewFilter(django_filters.FilterSet):
    class Meta:
        model =GuestReview
        fields =[
            'hotel',
            'staff',
            'facilities',
            'cleanliness',
            'comfort',
            'value_for_money',
            'location',
            'free_wifi',
        ]