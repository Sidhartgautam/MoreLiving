# rooms/serializers.py
from rest_framework import serializers
from .models import Room, RoomType, RoomImage, RoomAmenities
from hotels.models import Hotel

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [ 'id','type_name']

class RoomImageSerializer(serializers.ModelSerializer):
    # room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    # hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())

    class Meta:
        model = RoomImage
        fields = ['id', 'image']

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
    room_amenities = RoomAmenitiesSerializer(read_only=True, many=True, source='amenities')
    room_images = RoomImageSerializer(read_only=True, many=True, source='images')
    discounted_price = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_status', 'room_type', 'hotel', 'room_price', 'short_description', 'description', 'floor', 'room_amenities', 'room_images','bed_type', 'price_basis', 'inclusions', 'room_size', 'max_guests', 'discounted_price']

    def get_short_description(self, obj):
        if obj.description:
            return obj.description.split('.', 1)[0].strip()
        return None

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()

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
    
class RoomListSerializer(RoomSerializer):
    room_images = RoomImageSerializer(read_only=True, many=True, source='images')
    room_type=serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['id','room_type','room_number','room_price','room_images']

    def get_room_type(self, obj):
        return obj.room_type.type_name
    
class RoomDetailsSerializer(serializers.ModelSerializer):
    room_amenities = RoomAmenitiesSerializer(read_only=True, many=True, source='amenities')
    room_images = RoomImageSerializer(read_only=True, many=True, source='images')
    room_type=serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id','room_number','room_type','description','inclusions','room_amenities','room_price','room_images','price_basis','floor','max_guests','bed_type']

    def get_room_type(self, obj):
        return obj.room_type.type_name



