from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField(read_only=True)
    hotel_id = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all(), source='hotel')
    hotel_name = serializers.CharField(source='hotel.hotel_name', read_only=True)
    hotel_image=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Offer
        fields = ['id', 'hotel_id', 'hotel_name', 'hotel_image', 'title', 'description', 'discount_percentage', 'valid_from', 'valid_until','is_valid', 'is_active']

    def get_is_valid(self, obj):
        return obj.is_valid()

    def get_hotel_image(self, obj):
        # Get the first image related to the hotel, or return None if no image exists
        first_image = obj.hotel.images.first()
        if first_image:
            return first_image.image.url  # Return the URL of the first image
        return None