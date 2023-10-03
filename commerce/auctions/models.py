from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from decimal import Decimal


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass
# username, email, password, etc?? 
# Welcome to add aditional new filds

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category_name}"
    
class Listing(models.Model):
    """An item or listing """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True)
    image = models.CharField(max_length=200, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.PROTECT, related_name="category")
    date_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    watch = models.ManyToManyField(User, blank=True, related_name="watchlist")
    starting_price = models.FloatField(blank=True, default=0)
    current_bid = models.FloatField(blank=True, default=0)
    buyer = models.ForeignKey(User, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title}" f"{self.watch}"
    
    def is_watching(self, user):
        """ retruns true if the user is watching the listing (item)"""
        return user in self.watch.all()

    def add_to_watchlist(self, user):
        """ adds the user to the watch list (the user is now watching this item)"""
        self.watch.add(user)
        return True

    def remove_from_watchlist(self, user):
        """ removes the user from the watchlist (the user is not watching)"""
        self.watch.remove(user)
        return False

class Comments(models.Model):
    """All commens relates to the user who created it and to an item"""
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    item = models.ForeignKey(Listing, blank=True, default=0, on_delete=models.CASCADE, related_name="item_comment")
    date_comment = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}: {self.comment}"


class Bids(models.Model):
    """Each bid is saved with its own id"""
    id = models.AutoField(primary_key=True)
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_user")
    item = models.ForeignKey(Listing, blank=True, default=0, on_delete=models.CASCADE, related_name="item_bids")
    date_bid = models.DateTimeField(default=timezone.now)
    
    def total_bids(item_id):
        return len(Bids.objects.filter(item_id=item_id))