from datetime import date
from datetime import timedelta
from django import forms

ERROR_MSGS = {
    'required': 'Required',
    'invalid': 'Invalid'
}

class EntryForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages=ERROR_MSGS)
    minutes = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages=ERROR_MSGS)
    pages = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages=ERROR_MSGS)

    def clean_date(self):
        data = self.cleaned_data['date']
        
        today = date.today()
        offset = (today.weekday() - 5) % 7
        last_saturday = today - timedelta(days=offset)

        if data < last_saturday:
            raise forms.ValidationError('Too long ago')

        if data > today:
            raise forms.ValidationError('Future')

        return data
