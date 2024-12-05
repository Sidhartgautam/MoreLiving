# country/serializers.py
from rest_framework import serializers
from .models import Country, City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_code', 'currency']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_code', 'currency']

class PopularCitySerializer(serializers.ModelSerializer):
    hotel_count = serializers.SerializerMethodField()
    popular_count=serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'city_name', 'hotel_count', 'image', 'popular_count']

    def get_hotel_count(self, obj):
        return obj.hotels.count()

    def get_popular_count(self, obj):
        return obj.hotels.filter(city=obj).count()
    

