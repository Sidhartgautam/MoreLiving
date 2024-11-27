from rest_framework import serializers
from .models import HotelFAQ,WebsiteFAQ

class HotelFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelFAQ
        fields = ['id', 'question', 'answer']
        read_only_fields = ['id', 'created_at', 'updated_at']

class WebsiteFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteFAQ
        fields = ['id', 'question', 'answer']
        read_only_fields = ['id', 'created_at', 'updated_at']

