
from rooms.models import Room

def calculate_booking_price(validated_data):
    room = validated_data['room']
    check_in = validated_data['check_in']
    check_out = validated_data['check_out']
    duration = (check_out - check_in).days
    total_price = duration * room.room_price
    return total_price