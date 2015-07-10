from django import forms

class EntryForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    minutes = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    pages = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
