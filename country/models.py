from django.db import models
from currency.models import Currency

# Create your models here.
class Country(models.Model):
   country_name = models.CharField(max_length=50)
   country_code = models.CharField(max_length=50)
   currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

   def __str__(self):
       return f"{self.country_name}"