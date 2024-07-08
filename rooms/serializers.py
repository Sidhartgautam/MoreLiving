from rest_framework import serializers
from .models import Room, RoomType, RoomStatus, RoomImage, RoomAmenities
from hotels.serializers import HotelSerializer


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id','type_name']

class RoomStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomStatus
        fields = ['room_status']

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room', 'image']

class RoomAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAmenities
        fields = ['amenity_name']

class RoomSerializer(serializers.ModelSerializer):
    # room_type = RoomTypeSerializer(read_only=True)
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())
    room_status = serializers.PrimaryKeyRelatedField(queryset=RoomStatus.objects.all())
    room_amenities = RoomAmenitiesSerializer(read_only=True, many=True,source='amenities')
    room_images = RoomImageSerializer(read_only=True, many=True,source='images')

    class Meta:
        model = Room
        fields = ['id','room_number', 'room_status', 'room_type', 'hotel', 'room_price', 'description', 'floor', 'room_amenities', 'room_images']

