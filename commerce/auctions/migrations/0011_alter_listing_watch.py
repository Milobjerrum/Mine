# Generated by Django 4.2.5 on 2023-09-25 13:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0010_alter_listing_watch"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="watch",
            field=models.ManyToManyField(
                blank=True, related_name="watchlist", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
