from django import forms

class SearchForm(forms.Form):
    city = forms.CharField(label='city', max_length=50)
    state = forms.CharField(label='state', max_length=20)
    radius = forms.IntegerField(label='radius', max_value=200)

