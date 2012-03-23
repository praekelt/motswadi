from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView
from motswadi.models import NonAttendance, Teacher, Test
from motswadi.forms import RollCallForm, TestForm


class CreateTestView(CreateView):
    model = Test
    form_class = TestForm

    def get_form_kwargs(self):
        kwargs = super(CreateTestView, self).get_form_kwargs()
        kwargs['user'] = Teacher.objects.get(pk=self.request.user.pk)
        return kwargs


class RollCallView(FormView):
    form_class = RollCallForm
    template_name = 'motswadi/roll_call.html'
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.teacher = Teacher.objects.get(pk=request.user.pk)
        return super(RollCallView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        NonAttendance.objects.filter(date=date.today(), \
                student__in=self.teacher.student_set.all()).delete()
        for student in form.cleaned_data['students']:
            NonAttendance.objects.get_or_create(student=student, \
                    date=date.today())
        messages.success(self.request, 'Thank you. Roll call completed.')
        return super(RollCallView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(RollCallView, self).get_form_kwargs()
        kwargs.update({
            'teacher': self.teacher
        })
        return kwargs

    def get_initial(self):
        return {'students': [obj.student for obj in \
                NonAttendance.objects.filter(date=date.today())]}
