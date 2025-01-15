
from rooms.models import Room

# def calculate_booking_price(validated_data):
#     room = validated_data['room']
#     check_in = validated_data['check_in']
#     check_out = validated_data['check_out']
#     duration = (check_out - check_in).days
#     total_price = duration * room.room_price
#     return total_price


def calculate_booking_price(validated_data):
    check_in = validated_data['check_in']
    check_out = validated_data['check_out']
    duration = (check_out - check_in).days 
    hotel = validated_data['hotel']
    property_type = hotel.property_type.first()
    
    # Determine if whole-unit or room-based
    if property_type.is_whole_unit:
        room_price = hotel.rooms.first().room_price
    else:
        # Room-based booking: Use selected room's price
        room_price = validated_data['room'].room_price

    if property_type.type_name.lower() in ['apartment', 'villa', 'cottage']:
        # Long-term booking adjustments for whole-unit properties
        months = duration // 30  # 1 month = 30 days
        remaining_days = duration % 30
        weeks = remaining_days // 7  # 1 week = 7 days
        remaining_days = remaining_days % 7

        # Example price adjustments:
        monthly_rate = room_price * 25  # Adjusted monthly rate
        weekly_rate = room_price * 6  # Adjusted weekly rate
        daily_rate = room_price  # Standard daily rate

        total_price = (months * monthly_rate) + (weeks * weekly_rate) + (remaining_days * daily_rate)
        return total_price

    else:
        # Standard room-based bookings (hotels)
        return room_price * duration