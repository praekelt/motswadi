import re

from django import forms
from django.utils.safestring import mark_safe


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        """
        Render without ul and li containers. This is ugly :(
        """
        result = super(CustomCheckboxSelectMultiple, self).\
                render(name, value, attrs, choices=())
        return mark_safe(u'<br />'.join(re.findall('<label .*?</label>', \
                result, re.DOTALL)))
