# rooms/serializers.py
from rest_framework import serializers
from .models import Room, RoomType, RoomStatus, RoomImage, RoomAmenities
from hotels.models import Hotel

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'type_name']


class RoomStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomStatus
        fields = ['id', 'room_status']

class RoomImageSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())

    class Meta:
        model = RoomImage
        fields = ['id', 'room', 'image', 'hotel']

    def validate_room(self, value):
        if value.hotel != self.context['request'].user.hotel_set.first():
            raise serializers.ValidationError("The room must belong to the hotel associated with the current user.")
        return value

    def validate_image(self, value):
        if not value.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise serializers.ValidationError("Image must be a JPG, JPEG, PNG, or GIF.")
        return value


class RoomAmenitiesSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())

    class Meta:
        model = RoomAmenities
        fields = ['id', 'amenity_name', 'room', 'hotel']

    def validate_room(self, value):
        if value.hotel != self.context['request'].user.hotel_set.first():
            raise serializers.ValidationError("The room must belong to the hotel associated with the current user.")
        return value

    def validate_amenity_name(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Amenity name must be alphanumeric.")
        return value


class RoomSerializer(serializers.ModelSerializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())
    room_status = serializers.PrimaryKeyRelatedField(queryset=RoomStatus.objects.all())
    room_amenities = RoomAmenitiesSerializer(read_only=True, many=True, source='amenities')
    room_images = RoomImageSerializer(read_only=True, many=True, source='images')

    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_status', 'room_type', 'hotel', 'room_price', 'description', 'floor', 'room_amenities', 'room_images']

    def validate_room_number(self, value):
        hotel = self.context['request'].user.hotel_set.first()
        if not value.isalnum():
            raise serializers.ValidationError("Room number must be alphanumeric.")
        
        if Room.objects.filter(room_number=value, hotel=hotel).exists():
            raise serializers.ValidationError("A room with this number already exists in this hotel.")
        return value

    def validate(self, data):
        request = self.context.get('request')
        hotel = request.user.hotel_set.first()
        if data['hotel'] != hotel:
            raise serializers.ValidationError("The room must belong to the hotel associated with the current user.")
        if data['room_price'] <= 0:
            raise serializers.ValidationError("Room price must be positive.")
        return data


