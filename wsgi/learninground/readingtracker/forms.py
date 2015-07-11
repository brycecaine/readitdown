from django import forms

ERROR_MSGS = {
    'required': 'Required',
    'invalid': 'Invalid'
}

class EntryForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages=ERROR_MSGS)
    minutes = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages=ERROR_MSGS)
    pages = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages=ERROR_MSGS)
