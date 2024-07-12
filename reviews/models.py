import uuid
from django.db import models 
from hotels.models import Hotel
from users.models import User 


class Review(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(Hotel,related_name='reviews',on_delete=models.CASCADE)
    user =models.ForeignKey(User,related_name='reviews',on_delete=models.CASCADE)
    rating =models.PositiveIntegerField()
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.hotel.hotel_name}'



