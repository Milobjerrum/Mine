from django import forms
from .models import Listing#, Bids, Comments


class NewListingForm(forms.ModelForm):
    """Django form for new listing"""
    class Meta:
        model = Listing
        fields = [
            "title", 
            "description", 
            "image", 
            "starting_bid", 
        ]

