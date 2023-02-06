from django import forms
import datetime
from django.utils.safestring import mark_safe

class DurationFormField(forms.Field):
    def to_python(self, value):
        if not value:
            return None
        if isinstance(value, datetime.timedelta):
            value = str(value)
        parts = value.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        second = int(parts[2])
        return str(hours * 60 + minutes*60 +second)

class DurationWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = 0
        minutes = int(value / 60)
        hours = minutes // 60
        minutes = minutes % 60
        seconds = value - (hours * 3600 + minutes * 60)
        value = f'{hours}:{minutes}:{seconds}'
        return super().render(name, value, attrs)



class DurationUpdateWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = 0
        attrs['readonly'] = True
        minutes = int(value / 60)
        hours = minutes // 60
        minutes = minutes % 60
        html = f'{hours} hours, {minutes} minutes'
        return mark_safe(html)

