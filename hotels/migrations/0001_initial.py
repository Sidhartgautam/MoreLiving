# Generated by Django 5.0.7 on 2024-11-27 09:32

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelFacility',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('facility_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='media/hotel_images/')),
            ],
        ),
        migrations.CreateModel(
            name='HotelType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('hotel_name', models.CharField(max_length=50)),
                ('hotel_contact', models.CharField(max_length=50)),
                ('hotel_email', models.EmailField(max_length=254, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='country.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='country.country')),
            ],
        ),
    ]
