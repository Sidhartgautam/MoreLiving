from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Offer
        fields = ['id', 'hotel', 'title', 'description', 'discount_percentage', 'valid_from', 'valid_until','is_valid', 'is_active']

    def get_is_valid(self, obj):
        return obj.is_valid()