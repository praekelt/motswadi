from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, ListView, UpdateView
from motswadi.models import AssessmentResult, Event, NonAttendance, Teacher
from motswadi.forms import AssessmentResultForm, EventForm, RollCallForm

PAGINATE_BY = 10


class BaseView(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.teacher = Teacher.objects.get(pk=request.user.pk)
        return super(BaseView, self).\
                dispatch(request, *args, **kwargs)


class BaseFormView(object):
    def get_form_kwargs(self):
        kwargs = super(BaseFormView, self).get_form_kwargs()
        kwargs.update({
            'teacher': self.teacher
        })
        return kwargs


class CreateAssessmentResultView(BaseView, BaseFormView, CreateView):
    form_class = AssessmentResultForm
    template_name = 'motswadi/assessmentresult_form.html'
    success_url = '/'

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
                form.errors['__all__'].append('<strong><a href="%s">Update '\
                        'the existing assessment result here.</a></strong>' \
                        % reverse("update_assessment_result", \
                        kwargs={'pk': pk}))
        return super(CreateAssessmentResultView, self).form_invalid(form)


class CreateEventView(BaseView, BaseFormView, CreateView):
    model = Event
    success_url = '/'
    form_class = EventForm

    def form_valid(self, form):
        messages.success(self.request, 'Thank you. Event created.')
        return super(CreateEventView, self).form_valid(form)

    def form_invalid(self, form):
        if '__all__' in form.errors:
            if 'already exists' in ''.join(form.errors['__all__']):
                pk = Event.objects.get(
                    title=form.data['title'],
                    date="%s-%s-%s" % (form.data['date_year'], \
                            form.data['date_month'], form.data['date_day']),
                ).pk
                form.errors['__all__'].append('<strong><a href="%s">Update '\
                        'the existing event here.</a></strong>' % \
                        reverse("update_event", kwargs={'pk': pk}))
        return super(CreateEventView, self).form_invalid(form)

    def get_initial(self):
        return {'school': self.teacher.school.pk}


class RollCallView(BaseView, BaseFormView, FormView):
    form_class = RollCallForm
    template_name = 'motswadi/roll_call.html'
    success_url = '/'

    def form_valid(self, form):
        NonAttendance.objects.filter(date=date.today(), \
                student__in=self.teacher.student_set.all()).delete()
        for student in form.cleaned_data['students']:
            NonAttendance.objects.get_or_create(student=student, \
                    date=date.today())
        messages.success(self.request, 'Thank you. Roll call completed.')
        return super(RollCallView, self).form_valid(form)

    def get_initial(self):
        return {'students': [obj.student for obj in \
                NonAttendance.objects.filter(date=date.today())]}


class UpdateAssessmentResultView(BaseView, BaseFormView, UpdateView):
    form_class = AssessmentResultForm
    model = AssessmentResult
    template_name = 'motswadi/assessmentresult_update_form.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, 'Thank you. Assessment result updated.')
        return super(UpdateAssessmentResultView, self).form_valid(form)


class UpdateAssessmentResultsView(BaseView, ListView):
    model = AssessmentResult
    paginate_by = PAGINATE_BY


class UpdateEventView(BaseView, BaseFormView, UpdateView):
    model = Event
    template_name = 'motswadi/event_update_form.html'
    success_url = '/'
    form_class = EventForm

    def form_valid(self, form):
        messages.success(self.request, 'Thank you. Event updated.')
        return super(UpdateEventView, self).form_valid(form)


class UpdateEventsView(BaseView, ListView):
    model = Event
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return Event.objects.filter(school=self.teacher.school)
