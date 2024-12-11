from django.db import models
from django.utils import timezone
import uuid
from hotels.models import Hotel

class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255, help_text="Title of the offer (e.g., 'Winter Sale').")
    description = models.TextField(blank=True, null=True, help_text="Details about the offer.")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage.")
    valid_from = models.DateTimeField(help_text="Start date of the offer.")
    valid_until = models.DateTimeField(help_text="End date of the offer.")
    is_active = models.BooleanField(default=True, help_text="Set to false to deactivate the offer.")

    def is_valid(self):
        """Check if the offer is currently valid."""
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_until

    def __str__(self):
        return f"{self.title} - {self.hotel.hotel_name}"
