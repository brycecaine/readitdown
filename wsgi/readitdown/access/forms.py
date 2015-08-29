from access import service
from django import forms

GROUPS = (('', 'Select Role'),
         ('teacher', 'Teacher'),
         ('student', 'Student'),
    )

# ---------------------------------------------------------------------
# If form validation needs to happen on the file, try this:
# http://stackoverflow.com/a/20307970

class AddUsersForm(forms.Form):
    role = forms.ChoiceField(choices=GROUPS)
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddUsersForm, self).__init__(*args, **kwargs)
        if not service.is_manager(self.user):
            groups = (('', 'Select Role'),
                    ('student', 'Student'),
                )
            self.fields['role'] = forms.ChoiceField(choices=groups)

        self.fields['role'].widget.attrs['class'] = 'form-control'

    def clean_role(self):
        data = self.cleaned_data['role']

        # Only managers can create teacher accounts
        if not service.is_manager(self.user) and data == 'teacher':
            raise forms.ValidationError('Only managers can add teachers')

        return data
