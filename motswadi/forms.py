from django import forms
from django.forms.extras import SelectDateWidget
from django.forms.widgets import HiddenInput
from motswadi.models import AssessmentResult, Event, Student
from motswadi.widgets import CustomCheckboxSelectMultiple


class AssessmentResultForm(forms.ModelForm):
    class Meta:
        model = AssessmentResult

    def __init__(self, teacher, *args, **kwargs):
        super(AssessmentResultForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = self.fields['student'].\
                queryset.filter(school=teacher.school)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event

    def __init__(self, teacher, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = SelectDateWidget()
        self.fields['school'].label = ''
        self.fields['school'].widget = HiddenInput()
        self.fields['students'].queryset = self.fields['students'].\
                queryset.filter(school=teacher.school)


class RollCallForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Student.objects,
        widget=CustomCheckboxSelectMultiple
    )

    def __init__(self, teacher, *args, **kwargs):
        super(RollCallForm, self).__init__(*args, **kwargs)
        self.fields['students'].queryset = self.fields['students'].\
                queryset.filter(class_teacher=teacher)
