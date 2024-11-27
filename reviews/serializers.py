from rest_framework import serializers
from django.db.models import Avg
from django.db import models
from .models import GuestReview, HotelReview

class HotelReviewSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    class Meta:
        model = HotelReview
        fields = ['id', 'hotel', 'user', 'comment', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at', 'user','rating']

    def validate_rating(self, value):
        if value >= 10:
            raise serializers.ValidationError("Rating must be less than 10.")
        return value
    def create(self, validated_data):
        hotel = validated_data['hotel']
        guest_review_average = GuestReview.objects.filter(hotel=hotel).aggregate(
            avg_rating=Avg(
                (models.F('staff') + models.F('facilities') + models.F('cleanliness') +
                 models.F('comfort') + models.F('value_for_money') +
                 models.F('location') + models.F('free_wifi')) / 7
            )
        )['avg_rating']
        validated_data['rating'] = guest_review_average or 0
        return HotelReview.objects.create(user=self.context['request'].user, **validated_data)
    
    def get_review_count(self, obj):
        return GuestReview.objects.filter(hotel=obj.hotel).count()

class GuestReviewSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField() 
    category_averages = serializers.SerializerMethodField()

    class Meta:
        model = GuestReview
        fields = [
            'id', 'hotel', 'staff', 'facilities', 'cleanliness', 'comfort',
            'value_for_money', 'location', 'free_wifi', 'average_rating', 'category_averages', 'created_at'
        ]
        read_only_fields = ['id', 'average_rating', 'category_averages', 'created_at']

    def get_average_rating(self, obj):
        # Compute the average of all categories for a single review
        categories = ['staff', 'facilities', 'cleanliness', 'comfort', 'value_for_money', 'location', 'free_wifi']
        values = [getattr(obj, category) for category in categories]
        return sum(values) / len(values)

    def get_category_averages(self, obj):
        # Compute the averages of all reviews for this hotel, grouped by category
        reviews = GuestReview.objects.filter(hotel=obj.hotel)
        category_fields = ['staff', 'facilities', 'cleanliness', 'comfort', 'value_for_money', 'location', 'free_wifi']
        averages = {}
        for field in category_fields:
            averages[field] = reviews.aggregate(avg=models.Avg(field))[f'{field}__avg'] or 0
        return averages