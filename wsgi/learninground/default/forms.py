from django import forms

ROLES = (('', 'Select Role'),
         ('TCHR', 'Teacher'),
         ('STDN', 'Student'),
    )

class AddUsersForm(forms.Form):
    role = forms.ChoiceField(choices=ROLES)
    file = forms.FileField()
