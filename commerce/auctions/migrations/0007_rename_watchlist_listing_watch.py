# Generated by Django 4.2.5 on 2023-09-22 09:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_bids_date_bid_listing_watchlist"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="watchlist",
            new_name="watch",
        ),
    ]
