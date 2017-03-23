from django import forms
from .models import CityState

class SearchForm(forms.ModelForm):

    class Meta:
        model = CityState
        fields = ('city', 'state')