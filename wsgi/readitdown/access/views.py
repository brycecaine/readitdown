from access import service as access_service
from access.forms import AddUsersForm
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import FormView
import csv

class AddUsersView(FormView):
    template_name = 'access/add_users.html'
    form_class = AddUsersForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(AddUsersView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['is_manager'] = access_service.is_manager(self.request.user)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user = context.get('user')

        group_to_assign = form.cleaned_data.get('role', 'student')
        file = self.request.FILES['file']

        message = access_service.import_users(file, user, group_to_assign)
        messages.info(self.request, message)

        return super(AddUsersView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AddUsersView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

class UserTemplateView(View):
    def get(self, request, *args, **kwargs):
        kind = self.kwargs.get('kind', 'student')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_template.csv"' % kind

        writer = csv.writer(response)
        
        if kind == 'teacher':
            columns = ['email', 'first_name', 'last_name']
            data = ['teacher@example.com', 'First', 'Last']
        else:
            columns = ['email', 'first_name', 'last_name', 'guardian_email_1', 'guardian_email_2']
            data = ['student@example.com', 'First', 'Last', 'guard1@example.com', 'guard2@example.com']

        writer.writerow(columns)
        writer.writerow(data)

        return response
