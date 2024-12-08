import uuid
from django.db import models
from django.conf import settings
from hotels.models import Hotel
from rooms.models import Room
from django.core.exceptions import ValidationError
from django.utils import timezone
from notifications.models import Notification
from core.utils.notifications import send_notification_email

BookingStatusChoices = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    status = models.CharField(max_length=20, choices=BookingStatusChoices, default='pending')
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(null=True, blank=True)
    can_be_cancelled_until = models.DateTimeField(null=True, blank=True)
    num_adults = models.PositiveIntegerField(null=True, blank=True)
    num_children = models.PositiveIntegerField(null=True, blank=True)
    total_guests = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"
    
    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after check-in date.")
        
        if self.room.hotel != self.hotel:
            raise ValidationError("The selected room does not belong to the chosen hotel.")
        
        # Total number of guests validation
        num_adults = self.num_adults or 0
        num_children = self.num_children or 0
        total_guests = self.total_guests or 0
        if num_adults + num_children != total_guests:
            raise ValidationError("The total number of guests must be equal to the number of adults plus the number of children.")
        
        if total_guests > self.room.max_guests:
            raise ValidationError(f"The total number of guests cannot exceed the maximum number of {self.room.max_guests} allowed in the room.")

        # Check room availability for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            status="confirmed",  # Only consider confirmed bookings
            check_in__lt=self.check_out,  # Check if the check-in overlaps with another booking's check-out
            check_out__gt=self.check_in  # Check if the check-out overlaps with another booking's check-in
        ).exclude(id=self.id)  # Exclude the current booking from the check

        if overlapping_bookings.exists():
            raise ValidationError("The room is not available for the selected dates.")

        super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        message = f'New booking by {self.user.username} for room {self.room.id} from {self.check_in} to {self.check_out}'
        Notification.objects.create(
            user=self.user,
            hotel=self.room.hotel,
            message=message
        )
        send_notification_email(self.user.email, message)

    def cancel(self, reason):
        if self.can_be_cancelled_until and timezone.now() > self.can_be_cancelled_until:
            raise ValidationError("The cancellation period has passed.")
        self.is_cancelled = True
        self.cancellation_reason = reason
        self.save()
