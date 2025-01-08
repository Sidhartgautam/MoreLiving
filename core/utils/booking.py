
from rooms.models import Room

def calculate_booking_price(validated_data):
    room = validated_data['room']
    check_in = validated_data['check_in']
    check_out = validated_data['check_out']
    duration = (check_out - check_in).days
    total_price = duration * room.room_price
    return total_price


# def calculate_booking_price(validated_data):
#     room_price = validated_data['room'].room_price  # Base daily price
#     check_in = validated_data['check_in']
#     check_out = validated_data['check_out']
#     duration = (check_out - check_in).days  # Total number of days

#     property_type_name = validated_data['room'].hotel.property_type.first().type_name.lower()

#     if property_type_name in ['apartment', 'villa', 'cottage']:
#         # Calculate weeks and months
#         months = duration // 30  # Assuming 1 month = 30 days
#         remaining_days = duration % 30
#         weeks = remaining_days // 7
#         remaining_days = remaining_days % 7

#         # Example price adjustments:
#         monthly_rate = room_price * 25  # Discounted monthly rate (example)
#         weekly_rate = room_price * 6  # Discounted weekly rate (example)
#         daily_rate = room_price  # Standard daily rate

#         total_price = (months * monthly_rate) + (weeks * weekly_rate) + (remaining_days * daily_rate)
#         return total_price

#     else:  # Default for hotels (per night)
#         return room_price * duration