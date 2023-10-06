# Generated by Django 4.2.5 on 2023-10-06 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0022_rename_start_price_listing_starting_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="buyer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
