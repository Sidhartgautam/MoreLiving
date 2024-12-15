# rooms/models.py

from django.db import models
from hotels.models import Hotel
import uuid
from django.utils import timezone


ROOM_STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Under Maintenance'),
        ('unavailable', 'Unavailable'),
    ]


class RoomType(models.Model):
    hotel = models.ForeignKey("hotels.Hotel", on_delete=models.CASCADE,null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.type_name}-{self.hotel.hotel_name}"

class RoomImage(models.Model):
    hotel = models.ForeignKey("hotels.Hotel",on_delete=models.CASCADE,null=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="media/room_images/")

    def __str__(self):
        return f"{self.room.room_number} - Image"

class RoomAmenities(models.Model):
    hotel = models.ForeignKey("hotels.Hotel",on_delete=models.CASCADE,null=True)
    amenity_name = models.CharField(max_length=50)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="amenities",null=True)
    def __str__(self):
        return self.amenity_name

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_number = models.CharField(max_length=50)
    room_status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='available')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="rooms")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    bed_type = models.CharField(max_length=50, blank=True, null=True)
    price_basis=models.CharField(choices=[('per night', 'per night'), ('per person', 'per person')], default='per night', max_length=20)
    inclusions = models.TextField(null=True, blank=True)
    room_size = models.FloatField(null=True, blank=True, help_text="Size in square meters")
    room_price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    floor = models.IntegerField()
    max_guests = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Room {self.room_number} in {self.hotel.hotel_name} priced at {self.room_price}"
    def get_discounted_price(self):
        """
        Calculate the final room price based on any active offer for the hotel.
        """
        now = timezone.now()
        active_offer = self.hotel.offers.filter(
            is_active=True, valid_from__lte=now, valid_until__gte=now
        ).first()
        if active_offer:
            discount = (self.room_price * active_offer.discount_percentage) / 100
            return self.room_price - discount
        return self.room_price
