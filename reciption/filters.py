import django_filters
from django import forms

# models 
from reciption.models import Attendance
from reciption.models import SortLeave


class AttendanceFilters(django_filters.FilterSet):
    employee_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee ID'}))
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), label='From')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', widget=forms.DateInput(attrs={'type': 'date'}), label='To')

    class Meta:
        model = Attendance
        fields = ('employee_id','date')


class SortLeaveFilters(django_filters.FilterSet):
    employee_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee ID'}))
    ticket_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Ticket ID'}))
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), label='From')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', widget=forms.DateInput(attrs={'type': 'date'}), label='To')
    
    class Meta:
        model = SortLeave
        fields = ('employee_id', 'ticket_id', 'date',)
