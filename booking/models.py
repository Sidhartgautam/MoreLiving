import uuid
from django.db import models
from django.conf import settings
from hotels.models import Hotel
from rooms.models import Room
from django.core.exceptions import ValidationError
from django.utils import timezone
from notifications.models import Notification
from core.utils.notifications import send_notification_email

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
        
        #total number of guests
        if self.num_adults + self.num_children != self.total_guests:
            raise ValidationError("The total number of guests must be equal to the number of adults plus the number of children.")
        
        if self.total_guests > self.room.max_guests:
            raise ValidationError("The total number of guests cannot exceed the maximum number of {self.room.max_guests} allowed in the room.")

        # Check room availability
        existing_bookings = Booking.objects.filter(room=self.room, status__status="Confirmed").exclude(id=self.id)
        for booking in existing_bookings:
            if (self.check_in < booking.check_out and self.check_out > booking.check_in):
                raise ValidationError("The room is not available for the selected dates.")

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
