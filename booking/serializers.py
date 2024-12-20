from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'hotel', 'room', 'check_in', 'check_out', 'status','num_adults', 'num_children','total_guests','created_at','updated_at','is_cancelled', 'cancellation_reason', 'can_be_cancelled_until','payment_method']
        read_only_fields = ['user','created_at', 'updated_at','total_guests','is_cancelled', 'cancellation_reason', 'can_be_cancelled_until']

        #Check if the room is available or not for the selected dates

    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        # Check booking duration
        if (data['check_out'] - data['check_in']).days > 365:
            raise serializers.ValidationError("Booking duration cannot exceed one year.")
        
        # Check if room belongs to that hotel
        if data['room'].hotel != data['hotel']:
            raise serializers.ValidationError("The selected room does not belong to the chosen hotel.")
        
        # Total number of guests
        total_guests = data['num_adults'] + data['num_children']

        if total_guests > data['room'].max_guests:
            raise serializers.ValidationError(
                f"The total number of guests cannot exceed the maximum number of {data['room'].max_guests} allowed in the room."
            )

        # Check room availability
        existing_bookings = Booking.objects.filter(
            room=data['room'], 
            status="confirmed",  # Corrected here
            check_in__lt=data['check_out'], 
            check_out__gt=data['check_in']
        )
        if existing_bookings.exists():
            raise serializers.ValidationError("The room is not available for the selected dates.")
        
        data['total_guests'] = total_guests
        return data

    def create(self, validated_data):
        booking = Booking(**validated_data)
        booking.clean() 
        booking.save()
        return booking
