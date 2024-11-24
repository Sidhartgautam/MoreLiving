from django.db import models
from hotels.models import Hotel
from users.models import User
import uuid

# Create your models here.
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Notification for {self.hotel.hotel_name} - {self.message}"
