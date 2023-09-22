from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass
# username, email, password, etc?? 
# Welcome to add aditional new filds

class Listing(models.Model):
    """An item or listing """
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True)
    image = models.URLField(blank=True)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    date_created = models.DateTimeField(default=timezone.now)
    watch = models.ManyToManyField(User, related_name="watch")

    def __str__(self):
        return f"{self.title}"


class Bids(models.Model):
    """Each bid is saved with its own id"""
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    item = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="bids_item")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bids_user")
    date_bid = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"${self.amount}"


class Comments(models.Model):
    """All commens relates to the user who created it and to an item"""
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_comment")
    item = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="item_comment")
    date_comment = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}: {self.comment}"

