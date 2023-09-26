# Generated by Django 4.2.5 on 2023-09-25 10:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0009_alter_listing_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="watch",
            field=models.ManyToManyField(
                related_name="watchlist", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]