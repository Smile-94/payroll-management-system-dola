from django import forms

# models
from authority.models import OfficeTime



# Create form class here
class OfficeTimeForm(forms.ModelForm):
    office_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    office_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model=OfficeTime
        fields='__all__'