from default import service
from default.forms import AddUsersForm
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
import csv
import xlrd

class HomeView(TemplateView):
    template_name = 'default/home.html'

class AddUsersView(FormView):
    template_name = 'default/add_users.html'
    form_class = AddUsersForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(AddUsersView, self).get_context_data(**kwargs)
        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user = context.get('user')

        group_to_assign = form.cleaned_data.get('group', 'student')
        # Only administrators can create teacher accounts
        if service.is_manager(user) and group_to_assign == 'teacher':
            group_to_assign = 'student'

        file = self.request.FILES['file']
        content_type = self.request.FILES['file'].content_type

        # ---------------------------------------------------------------------
        # There needs to be some validation here so the right parsing can
        # happen depending on the file type. But if form validation needs to
        # happen on the file, try this: http://stackoverflow.com/a/20307970

        # Handle CSVs
        if content_type == 'text/csv':
            reader = csv.reader(file)
            header_row = reader.next()
            for row in reader:
                user_data = {
                    'email': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'group_name': group_to_assign
                }

                new_user = service.create_user(**user_data)
                
                if service.is_teacher(user):
                    friendship = service.create_friendship(new_user, user, True, 'teacher')

                for guardian_email in row[3:]:
                    guardian_data = {
                        'email': guardian_email,
                        'group_name': 'guardian'
                    }
                    guardian = service.create_user(**guardian_data)
                    friendship = service.create_friendship(new_user, guardian, True, 'guardian')

            file.close()

            messages.success(self.request, 'Import successful')

        # Handle Excel files
        elif content_type in ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'):
            workbook = xlrd.open_workbook(filename=None, file_contents=file.read())
            sh = workbook.sheet_by_index(0)
            for rx in range(sh.nrows)[1:]:
                row = sh.row(rx)
                user_data = {
                    'email': row[0].value,
                    'first_name': row[1].value,
                    'last_name': row[2].value,
                    'group_name': group_to_assign
                }

                print user_data
                new_user = service.create_user(**user_data)

                if service.is_teacher(user):
                    friendship = service.create_friendship(new_user, user, True, 'teacher')

                for cell in row[3:]:
                    guardian_email = cell.value
                    guardian_data = {
                        'email': guardian_email,
                        'group_name': 'guardian'
                    }
                    print guardian_data
                    guardian = service.create_user(**guardian_data)
                    friendship = service.create_friendship(new_user, guardian, True, 'guardian')

            messages.success(self.request, 'Import successful')

        else:
            messages.error(self.request, 'Import failed')

        return super(AddUsersView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AddUsersView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs
