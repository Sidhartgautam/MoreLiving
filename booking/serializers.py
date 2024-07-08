from rest_framework import serializers
from .models import Booking, BookingStatus

class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingStatus
        fields = ['id', 'status']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'hotel', 'room', 'check_in', 'check_out', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

        #Check if the room is available or not for the selected dates

    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        #Check if room belongs to that hotel or not
        
        if data['room'].hotel != data['hotel']:
            raise serializers.ValidationError("The selected room does not belong to the chosen hotel.")

        # Check room availability
        existing_bookings = Booking.objects.filter(room=data['room'], status__status="Confirmed")
        for booking in existing_bookings:
            if (data['check_in'] < booking.check_out and data['check_out'] > booking.check_in):
                raise serializers.ValidationError("The room is not available for the selected dates.")
        
        return data

    def create(self, validated_data):
        booking = Booking(**validated_data)
        booking.clean()  # This will run the clean method from the model
        booking.save()
        return booking
