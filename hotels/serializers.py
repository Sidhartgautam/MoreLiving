from  rest_framework import serializers
from .models import Hotel, HotelType, HotelFacility, HotelImage
from reviews.models import HotelReview
from rooms.serializers import RoomSerializer
from django.db.models import Avg
from django.db import models
from booking.models import Booking
from django.utils.dateparse import parse_datetime

class HotelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelType
        fields = ['id', 'type_name']

class HotelFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelFacility
        fields = [ 'facility_name']

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['image']

class HotelSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    short_description = serializers.SerializerMethodField(read_only=True)
    city_name = serializers.SerializerMethodField(read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    facilities = HotelFacilitySerializer(many=True, read_only=True)
    rooms = serializers.SerializerMethodField(read_only=True)  # Dynamically filter rooms

    class Meta:
        model = Hotel
        fields = [
            'id', 'hotel_name', 'city', 'city_name', 'address', 'rating',
            'short_description', 'review_count', 'facilities', 'images', 'rooms'
        ]

    def get_rating(self, obj):
        avg_rating = HotelReview.objects.filter(hotel=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return avg_rating or 0

    def get_review_count(self, obj):
        count = HotelReview.objects.filter(hotel=obj).count()
        return count

    def get_short_description(self, obj):
        if obj.description:
            return obj.description.split('.', 1)[0].strip()
        return None

    def get_city_name(self, obj):
        return obj.city.city_name

    def get_rooms(self, obj):
        request = self.context.get('request')
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')

        if check_in and check_out:
            try:
                # Parse check-in and check-out dates
                check_in_date = parse_datetime(check_in)
                check_out_date = parse_datetime(check_out)

                # Find unavailable rooms
                unavailable_room_ids = Booking.objects.filter(
                    status="confirmed",
                    check_in__lt=check_out_date,
                    check_out__gt=check_in_date
                ).values_list('room_id', flat=True)
                available_rooms = obj.rooms.exclude(id__in=unavailable_room_ids)
            except ValueError:
                available_rooms = obj.rooms.all()
        else:
            available_rooms = obj.rooms.all()

        return RoomSerializer(available_rooms, many=True).data


class HotelDetailSerializer(HotelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    city_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Hotel
        fields = [
            'id', 'hotel_name', 'city', 'city_name', 'address','lat', 'lng', 'rating',
            'short_description', 'review_count', 'facilities', 'images', 'rooms'
        ]

    def get_city_name(self, obj):
        return obj.city.city_name


    
