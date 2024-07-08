from django.db import models

# Create your models here.
class Permission(models.Model):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name