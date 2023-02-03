from django.forms import widgets
from django.utils.safestring import mark_safe
from string import Template


class CustomPictureImageFieldWidget(widgets.FileInput):

    def render(self, name, value, attrs=None,renderer=None, **kwargs):
        default_html = super().render(name, value, attrs=None, **kwargs)
        img_html = ''
        if value and hasattr(value, 'url'):
            img_html = mark_safe(f'<img src="{value.url}" height="150" width="130">')
        return f'{img_html}{default_html}'


class CustomSignetureImageFieldWidget(widgets.FileInput):

    def render(self, name, value, attrs=None,renderer=None, **kwargs):
        default_html = super().render(name, value, attrs=None, **kwargs)
        img_html = ''
        if value and hasattr(value, 'url'):
            img_html = mark_safe(f'<img src="{value.url}" height="80" width="130">')
        return f'{img_html}{default_html}'