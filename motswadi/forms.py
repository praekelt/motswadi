from django import forms
from django.forms.extras import SelectDateWidget
from motswadi.models import Event, Student
from motswadi.widgets import CustomCheckboxSelectMultiple


class EventForm(forms.ModelForm):
    class Meta:
        model = Event

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = SelectDateWidget()


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
