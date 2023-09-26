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
        ]
        
        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(),
            "image": forms.TextInput(),
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
            "bid": forms.NumberInput(attrs={"class": "form-controle"})
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

