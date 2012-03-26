from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, UpdateView
from motswadi.models import AssessmentResult, NonAttendance, Teacher
from motswadi.forms import RollCallForm


class CreateAssessmentResultView(CreateView):
    model = AssessmentResult
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAssessmentResultView, self).\
                dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Thank you. Assessment result created.')
        return super(CreateAssessmentResultView, self).form_valid(form)

    def form_invalid(self, form):
        if '__all__' in form.errors:
            if 'already exists' in ''.join(form.errors['__all__']):
                pk = AssessmentResult.objects.get(
                    title=form.data['title'],
                    subject=form.data['subject'],
                    student=form.data['student']
                ).pk
                form.errors['__all__'].append('<a href="%s">Update the "\
                        "existing assessment result here.</a>' % \
                        reverse("update_assessment_result", kwargs={'pk': pk}))
        return super(CreateAssessmentResultView, self).form_invalid(form)


class UpdateAssessmentResultView(UpdateView):
    model = AssessmentResult
    template_name = 'motswadi/assessmentresult_update_form.html'
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateAssessmentResultView, self).\
                dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Thank you. Assessment result updated.')
        return super(UpdateAssessmentResultView, self).form_valid(form)


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
