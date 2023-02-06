from django import forms

# Widgets 
from reciption.widgets import DurationWidget
from reciption.widgets import DurationFormField
from reciption.widgets import DurationUpdateWidget

# models
from reciption.models import Attendance
from reciption.models import SortLeave


class AttendanceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    entering_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    exit_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Attendance
        exclude = ('attendance_of',)


class SortLeaveForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    outing_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    leave_hour = DurationFormField(widget=DurationWidget)
    
    class Meta:
        model = SortLeave
        fields = ('employee_id', 'date', 'leave_hour', 'outing_time', 'description')
       
        


class SortLeaveUpdateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    outing_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    entering_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    
    class Meta:
        model = SortLeave
        fields = ('employee_id', 'date', 'leave_hour', 'outing_time', 'entering_time')

        widgets = {
            'duration': DurationUpdateWidget
        }
