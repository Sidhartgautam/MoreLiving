# Generated by Django 5.0.7 on 2024-11-27 09:32

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('is_cancelled', models.BooleanField(default=False)),
                ('cancellation_reason', models.TextField(blank=True, null=True)),
                ('can_be_cancelled_until', models.DateTimeField(blank=True, null=True)),
                ('num_adults', models.PositiveIntegerField(blank=True, null=True)),
                ('num_children', models.PositiveIntegerField(blank=True, null=True)),
                ('total_guests', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]
