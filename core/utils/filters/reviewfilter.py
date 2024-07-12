import django_filters
from reviews.models import Review

class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model =Review
        fields =['hotel','user','rating']