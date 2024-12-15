# Generated by Django 5.0.7 on 2024-12-15 06:14

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('room_number', models.CharField(max_length=50)),
                ('room_status', models.CharField(choices=[('available', 'Available'), ('booked', 'Booked'), ('maintenance', 'Under Maintenance'), ('unavailable', 'Unavailable')], default='available', max_length=20)),
                ('bed_type', models.CharField(blank=True, max_length=50, null=True)),
                ('price_basis', models.CharField(choices=[('per night', 'per night'), ('per person', 'per person')], default='per night', max_length=20)),
                ('inclusions', models.TextField(blank=True, null=True)),
                ('room_size', models.FloatField(blank=True, help_text='Size in square meters', null=True)),
                ('room_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('description', models.TextField()),
                ('floor', models.IntegerField()),
                ('max_guests', models.PositiveIntegerField(blank=True, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotels.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='RoomAmenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity_name', models.CharField(max_length=50)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.hotel')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amenities', to='rooms.room')),
            ],
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/room_images/')),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.hotel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='rooms.room')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=20)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.hotel')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='rooms.roomtype'),
        ),
    ]
