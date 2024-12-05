from  rest_framework import serializers
from .models import Hotel, HotelType, HotelFacility, HotelImage
from reviews.models import HotelReview
from rooms.serializers import RoomSerializer
from django.db.models import Avg

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
    city_name=serializers.SerializerMethodField(read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    facilities = HotelFacilitySerializer(many=True, read_only=True)
    rooms=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name','city','city_name','address', 'rating','short_description', 'review_count', 'facilities', 'images','rooms']

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
        rooms = obj.rooms.all()[:5] 
        return RoomSerializer(rooms, many=True).data


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_type = serializers.ListField(child=serializers.UUIDField(), write_only=True)
    hotel_email = serializers.EmailField(required=True)
    hotel_contact = serializers.CharField(required=True)
    hotel_images = HotelImageSerializer(read_only=True, many=True, source='images')
    hotel_facilities = HotelFacilitySerializer(read_only=True, many=True, source='facilities')
    class Meta:
        model = Hotel
        fields = ['id','hotel_name','hotel_email','hotel_contact','hotel_type','country','address','city','state','lng','lat','updated_at','user','hotel_images','hotel_facilities']
        read_only_fields = ['id', 'updated_at','user']

    def validate(self, data):
        user = self.context['request'].user
        if Hotel.objects.filter(user=user).exists():
            raise serializers.ValidationError("A user can only add one hotel.")
        if data['lng'] < -180 or data['lng'] > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180 degrees.")
        if data['lat'] < -90 or data['lat'] > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90 degrees.")
        return data

    def create(self, validated_data):
        hotel_types_data = validated_data.pop('hotel_type')
        hotel = Hotel.objects.create(**validated_data)
        hotel_types = HotelType.objects.filter(id__in=hotel_types_data)
        hotel.hotel_type.set(hotel_types)
        return hotel
    
class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name','city']


    
