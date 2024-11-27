from django.db import models
from hotels.models import Hotel
import uuid
from core.utils.models import TimestampedModel,UUIDModel

# Create your models here.
class HotelFAQ(TimestampedModel, UUIDModel):
    hotel = models.ForeignKey(
        Hotel, 
        on_delete=models.CASCADE, 
        related_name="faqs",
        help_text="The hotel to which this FAQ belongs"
    )
    question = models.CharField(max_length=255, help_text="FAQ question for the hotel")
    answer = models.TextField(help_text="FAQ answer for the hotel")


    def __str__(self):
        return f"FAQ for {self.hotel.hotel_name}: {self.question[:50]}"
    
class WebsiteFAQ(TimestampedModel,UUIDModel):
    question = models.CharField(max_length=255, help_text="FAQ question for the website")
    answer = models.TextField(help_text="FAQ answer for the website")

    
    def __str__(self):
        return f"Website FAQ: {self.question[:50]}"
