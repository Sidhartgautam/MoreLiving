# Generated by Django 5.0.7 on 2024-12-23 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=50)),
                ('currency_code', models.CharField(max_length=50)),
                ('currency_symbol', models.CharField(max_length=50)),
            ],
        ),
    ]
