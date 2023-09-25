from django import forms
from .models import Listing, Comments


class NewListingForm(forms.ModelForm):
    """Django form for new listing"""
    class Meta:
        model = Listing
        fields = [
            "title", 
            "description", 
            "image", 
            "price"
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Give your listing a title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Write a description"}), 
            "image": forms.TextInput(attrs={"class": "form-control", "placeholder": "Add a image URL "}), 
            "price": forms.TextInput(attrs={"class": "form-control", "placeholder": "Starting price "}), 
        }

class CommentsForm(forms.ModelForm):
    """Comments on items"""
    class Meta:
        model = Comments
        fields = ["comment"]

        widgets = {
            "comment": forms.TextInput(attrs={"class": "form-controle", "placeholder": "Be nice"}),
        }