from django.forms import ModelForm
from .models import Listing, Comments


class NewListingForm(ModelForm):
    """Django form for new listing"""
    class Meta:
        model = Listing
        fields = [
            "title", 
            "description", 
            "image", 
            "price", 
        ]

class CommentsForm(ModelForm):
    """Comments on items"""
    class Meta:
        model = Comments
        fields = [
            "comment"
        ]
        labels = {
            "comment": ""
        }