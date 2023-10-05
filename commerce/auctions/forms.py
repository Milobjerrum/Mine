from typing import Any
from django import forms
from .models import Listing, Comments, Bids



class NewListingForm(forms.ModelForm):
    """Django form for new listing"""
    class Meta:
        model = Listing
        fields = [
            "title", 
            "description", 
            "image", 
            "category",
            "starting_price"        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget = forms.TextInput(attrs={
            "class": "form-control", "placeholder": "Listing title"
        })
        self.fields["description"].widget = forms.Textarea(attrs={
            "class": "form-control", "placeholder": "Give the listing a description"
        })
        self.fields["image"].widget = forms.TextInput(attrs={
            "class": "form-control", "placeholder": "image url"
        })

        self.fields["starting_price"].widget = forms.TextInput(attrs={
            "class": "form-control",
        })
            


class CommentsForm(forms.ModelForm):
    """Comments on items"""
    class Meta:
        model = Comments
        fields = ["comment"]

        widgets = {
            "comment": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            css = {
                "placeholder": f"{str(field).title()}",
                "class": "form-control"
        }
            self.fields[str(field)].widget.attrs.update(
                css
            )
            self.fields[str(field)].label = ""

class PlaceBidForm(forms.ModelForm):
    """Place bids"""
    class Meta:
        model = Bids
        fields = ["bid"]

        widgets = {
            "bid": forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            css = {
                "placeholder": f"{str(field).title()}",
                "class": "form-control"
        }
            self.fields[str(field)].widget.attrs.update(
                css
            )
            self.fields[str(field)].label = ""


