import uuid
from django.db import models 
from hotels.models import Hotel
from users.models import User
from django.core.exceptions import ValidationError 


class HotelReview(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(Hotel, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class GuestReview(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(Hotel, related_name='guest_reviews', on_delete=models.CASCADE)
    staff = models.FloatField()
    facilities = models.FloatField()
    cleanliness = models.FloatField()
    comfort = models.FloatField()
    value_for_money = models.FloatField()
    location = models.FloatField()
    free_wifi = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Validates that all numerical fields have values less than 10.
        """
        fields_to_validate = [
            ('staff', self.staff),
            ('facilities', self.facilities),
            ('cleanliness', self.cleanliness),
            ('comfort', self.comfort),
            ('value_for_money', self.value_for_money),
            ('location', self.location),
            ('free_wifi', self.free_wifi)
        ]

        for field_name, value in fields_to_validate:
            if value >= 10:
                raise ValidationError({field_name: f"{field_name.replace('_', ' ').capitalize()} must be less than 10."})

    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation before saving
        self.clean()
        super().save(*args, **kwargs)



