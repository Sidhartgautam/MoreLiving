from django.db import models
from hotels.models import Hotel
import uuid

class HouseRule(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.OneToOneField(
        Hotel,
        on_delete=models.CASCADE,
        related_name="house_rule",
        help_text="Hotel to which this house rule applies"
    )
    check_in_time = models.TimeField(null=True, blank=True, help_text="Earliest check-in time")
    check_out_time = models.TimeField(null=True, blank=True, help_text="Latest check-out time")
    cancellation_policy = models.TextField(
        null=True, 
        blank=True, 
        help_text="Details about the cancellation and prepayment policies"
    )
    children_allowed = models.BooleanField(
        default=True, 
        help_text="Whether children are allowed"
    )
    crib_policy = models.TextField(
        null=True, 
        blank=True, 
        help_text="Policy regarding cribs (e.g., ages, costs)"
    )
    extra_bed_policy = models.TextField(
        null=True, 
        blank=True, 
        help_text="Policy regarding extra beds (e.g., costs, availability)"
    )
    age_restriction = models.BooleanField(
        default=False,
        help_text="Whether there is an age restriction for check-in"
    )
    age_restriction_details = models.TextField(
        null=True, 
        blank=True, 
        help_text="Details about age restrictions, if applicable"
    )
    additional_rules = models.TextField(
        null=True, 
        blank=True, 
        help_text="Any additional house rules"
    )

    def __str__(self):
        return f"House Rules for {self.hotel.hotel_name}"