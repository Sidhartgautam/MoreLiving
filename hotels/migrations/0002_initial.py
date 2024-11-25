# Generated by Django 5.1.3 on 2024-11-24 09:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotelfacility',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facilities', to='hotels.hotel'),
        ),
        migrations.AddField(
            model_name='hotelimage',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='hotels.hotel'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_type',
            field=models.ManyToManyField(blank=True, related_name='hotels', to='hotels.hoteltype'),
        ),
    ]
