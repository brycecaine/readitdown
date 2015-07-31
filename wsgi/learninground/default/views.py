from default import service
from default.forms import AddUsersForm
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
        print 'context'
        # print context['form'].fields
        # print context['form'].fields['file']
        # print context['form'].fields['file'].__dict__

        return context

    def form_valid(self, form):
        print 'valid form'
        role = form.cleaned_data.get('role', 'student')
        file = self.request.FILES['file']
        content_type = self.request.FILES['file'].content_type
        print file

        # ---------------------------------------------------------------------
        # There needs to be some validation here so the right parsing can
        # happen depending on the file type. But if form validation needs to
        # happen on the file, try this: http://stackoverflow.com/a/20307970

        # Handle CSVs
        if content_type == 'text/csv':
            reader = csv.reader(file)
            for row in reader:
                email = row[0]
                user = service.create_user(email, role)
                row.pop(0)
                for guardian_email in row:
                    guardian = service.create_guardian(user, guardian_email)

            file.close()

        # Handle Excel files
        elif content_type in ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'):
            workbook = xlrd.open_workbook(filename=None, file_contents=file.read())
            sh = workbook.sheet_by_index(0)
            for rx in range(sh.nrows):
                row = sh.row(rx)
                email = row[0].value
                user = service.create_user(email, role)
                row.pop(0)
                for cell in row:
                    guardian_email = cell.value
                    guardian = service.create_guardian(user, guardian_email)

        else:
            print 'invalid file'

        return super(AddUsersView, self).form_valid(form)
