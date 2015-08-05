from default import service
from django import forms

GROUPS = (('', 'Select Role'),
         ('teacher', 'Teacher'),
         ('student', 'Student'),
    )

class AddUsersForm(forms.Form):
    role = forms.ChoiceField(choices=GROUPS)
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddUsersForm, self).__init__(*args, **kwargs)
        if service.is_teacher(user):
            groups = (('', 'Select Role'),
                    ('student', 'Student'),
                )
            self.fields['role'] = forms.ChoiceField(choices=groups)
