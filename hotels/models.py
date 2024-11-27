from django.db import models
from country.models import Country
import uuid
from django.conf import settings
from users.models import User

class PropertyType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.type_name}"

# Create your models here.
class HotelType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.type_name}"
    

class Hotel(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   hotel_name = models.CharField(max_length=50)
   hotel_contact = models.CharField(max_length=50)
   hotel_email = models.EmailField(null=True)
   description = models.TextField(null=True,blank=True)
   hotel_type = models.ManyToManyField(HotelType, blank=True,related_name='hotels') 
   property_type = models.ManyToManyField(PropertyType, blank=True,related_name='hotels')
   country = models.ForeignKey(Country, on_delete=models.CASCADE)
   address = models.CharField(max_length=50)
   city = models.CharField(max_length=50)
   state = models.CharField(max_length=50)
   lng = models.DecimalField(max_digits=9, decimal_places=6)
   lat = models.DecimalField(max_digits=9, decimal_places=6)
   updated_at = models.DateTimeField(auto_now=True, null=True)
   user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

   def __str__(self):
       return f"{self.hotel_name}"
   
class HotelFacility(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(Hotel, related_name='facilities', on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.facility_name} - {self.hotel.hotel_name}"
    
class HotelImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/hotel_images/')

    def __str__(self):
        return f"Image for {self.hotel.hotel_name}"

   
   

    
