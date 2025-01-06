
from rooms.models import Room

def calculate_booking_price(validated_data):
    room = validated_data['room']
    check_in = validated_data['check_in']
    check_out = validated_data['check_out']
    duration = (check_out - check_in).days
    total_price = duration * room.room_price
    return total_price


# def calculate_booking_price(validated_data):
#     room_price = validated_data['room'].room_price
#     check_in = validated_data['check_in']
#     check_out = validated_data['check_out']
#     duration = (check_out - check_in).days

#     property_type_name = validated_data['room'].hotel.property_type.first().type_name.lower()

#     if property_type_name == 'apartment':
#         return room_price * duration  # Price per day
#     elif property_type_name == 'villa':
#         weeks = duration // 7
#         remaining_days = duration % 7
#         weekly_rate = room_price * 7  # Example: assuming weekly discount
#         return (weeks * weekly_rate) + (remaining_days * room_price)
#     else:  # Default is per night (hotel)
#         return room_price * duration