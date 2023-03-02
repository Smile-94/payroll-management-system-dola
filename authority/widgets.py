from django import forms
from datetime import timedelta
from django.utils.safestring import mark_safe

class DurationFormField(forms.Field):
    def to_python(self, value):
        if not value:
            return None
        if isinstance(value, timedelta):
            value = str(value)
        parts = value.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

class DurationWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = timedelta(0)
        elif isinstance(value, int):
            value = timedelta(seconds=value)
        elif isinstance(value, str):
            parts = value.split(':')
            value = timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
        minutes, seconds = divmod(value.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        value = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
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

