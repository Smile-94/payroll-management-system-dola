from django import forms
from datetime import datetime

# Customs Widgets
from authority.widgets import DurationWidget
from authority.widgets import DurationFormField

# models
from authority.models import OfficeTime
from authority.models import PayrollMonth
from authority.models import FestivalBonus
from authority.models import LeaveApplication
from authority.models import MonthlyOffDay
from authority.models import MonthlyHoliday
from authority.models import MonthlyPermitedLeave
from authority.models import PermitedLatePresent
from authority.models import PermitedSortLeave
from authority.models import WeeklyOffday
from authority.models import Notice



# Create form class here
class PayrollMonthForm(forms.ModelForm):
    current_year = datetime.now().year
    year_choices = [(year, year) for year in range(current_year-5, current_year+5)]
    year = forms.ChoiceField(choices=year_choices)
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = PayrollMonth
        fields = ('month','year','from_date','to_date')

class OfficeTimeForm(forms.ModelForm):
    
    office_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    office_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model=OfficeTime
        fields = '__all__'


class FestivalBonusForm(forms.ModelForm):

    class Meta:
        model=FestivalBonus
        exclude=('is_active',)


class LeaveApplicationForm(forms.ModelForm):
    leave_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    leave_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LeaveApplication
        fields =('leave_from','leave_to','leave_description')


class LeavApplicationAcceptForm(forms.ModelForm):
    leave_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    leave_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LeaveApplication
        fields =( 'leave_from','leave_to',)

class LeaveApplicationRejectForm(forms.ModelForm):

    class Meta:
        model = LeaveApplication
        fields = ('declined_message',)
        

class MonthlyOffDayForm(forms.ModelForm):

    class Meta:
        model = MonthlyOffDay
        fields = ('month','total_offday',)


class MonthlyHolidayForm(forms.ModelForm):
    holiday_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = MonthlyHoliday
        fields = ('holiday_month','holiday_name','holiday_date')


class MonthlyPermitedLeaveForm(forms.ModelForm):

    class Meta:
        model = MonthlyPermitedLeave
        fields = ('leave_month','permited_days','salary_diduction')


class PermitedLatePresentForm(forms.ModelForm):
    peremited_time = DurationFormField(widget=DurationWidget)

    class Meta:
        model = PermitedLatePresent
        fields = ('peremited_time','permited_days','salary_diduction')


class PermitedSortLeaveForm(forms.ModelForm):
    class Meta:
        model = PermitedSortLeave
        fields = ('permited_days','salary_diduction')


class WeeklyOffdayForm(forms.ModelForm):

    class Meta:
        model = WeeklyOffday
        fields = ('first_day','second_day')

class NoticeForm(forms.ModelForm):

    class Meta:
        model = Notice
        fields = ('subject','description')
    