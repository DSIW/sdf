from django import forms

from django.forms import ModelForm
from django import forms
from django.http import HttpRequest

from .models import SellerRating

class RateSellerForm(ModelForm):
    rating = forms.NumberInput()
    textrating = forms.TextInput()

    def __init__(self, *args, **kwargs):
        super(RateSellerForm, self).__init__(*args, **kwargs)
        self.fields['textrating'].label = "Hinterlassen Sie ein Kommentar zum Verkäufer."

    class Meta:
        model=SellerRating
        fields = ['rating','textrating',]
        widgets = {
            'rating' : forms.HiddenInput(),
        }
