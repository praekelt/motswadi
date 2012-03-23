from django import forms
from motswadi.models import Student, Test
from motswadi.widgets import CustomCheckboxSelectMultiple


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


class TestForm(forms.ModelForm):
    class Meta:
        model = Test

    def __init__(self, user, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = user.subjects.all()
