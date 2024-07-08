import uuid
from django.db import models
from django.conf import settings
from hotels.models import Hotel
from rooms.models import Room
from django.core.exceptions import ValidationError
from django.utils import timezone

class BookingStatus(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    status = models.ForeignKey(BookingStatus, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"
    
    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after check-in date.")
        
        if self.room.hotel != self.hotel:
            raise ValidationError("The selected room does not belong to the chosen hotel.")

        # Check room availability
        existing_bookings = Booking.objects.filter(room=self.room, status__status="Confirmed").exclude(id=self.id)
        for booking in existing_bookings:
            if (self.check_in < booking.check_out and self.check_out > booking.check_in):
                raise ValidationError("The room is not available for the selected dates.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def cancel(self, reason):
        if self.can_be_cancelled_until and timezone.now() > self.can_be_cancelled_until:
            raise ValidationError("The cancellation period has passed.")
        self.is_cancelled = True
        self.cancellation_reason = reason
        self.save()
