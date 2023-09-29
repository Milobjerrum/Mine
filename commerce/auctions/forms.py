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
            "category",        ]
        
        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "image": forms.TextInput(),
            "category": forms.Select(),
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
            "bid": forms.TextInput(),
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

    def clean_bid(self):
        super().clean()
        bid = self.cleaned_data.get("bid")
        item_id = self.instance.item_id #Get the item id associated with the bid

        # Check if the bid is higher than the current highest bid
        highest_bid = Bids.highest_bid(item_id)
        if bid <= highest_bid:
            raise forms.ValidationError("")
        
        return bid

