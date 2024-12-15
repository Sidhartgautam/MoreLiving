from django.db import models
from hotels.models import Hotel
from core.utils.models import UUIDModel,TimestampedModel



class HotelFAQ(TimestampedModel,UUIDModel):
    hotel = models.ForeignKey(
        Hotel, 
        on_delete=models.CASCADE, 
        related_name="faqs",
        help_text="The hotel to which this FAQ belongs"
    )
    question_text = models.TextField()
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name="replies", 
        null=True, 
        blank=True,
        help_text="Parent FAQ if this is a reply"
    )
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name="hotel_faqs",
        help_text="User who created this FAQ"
    )

    def __str__(self):
        if self.parent:
            return f"Reply to: {self.parent.question_text[:50]}"
        return f"Question: {self.question_text[:50]}"


class MoreLivingFAQ(TimestampedModel, UUIDModel):
    question_text = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
        help_text="Parent FAQ if this is a reply"
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="website_faqs",
        help_text="User who created this FAQ"
    )

    def __str__(self):
        if self.parent:
            return f"Reply to: {self.parent.question_text[:50]}"
        return f"Question: {self.question_text[:50]}"