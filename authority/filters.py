import django_filters
from django import forms
from datetime import datetime

from accounts.models import User
from employee.models import EmployeeInfo
from employee.models import DesignationInfo
from authority.models import PayrollMonth
from authority.models import LeaveApplication


class EmployeeListFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = {
            'email': {'exact'},
        }


class SalaryEmployeeFilters(django_filters.FilterSet):
    DEPARTMENT_OPT = (
    ('HR', 'Human Resource'),
    ('administrative', 'Administrative'),
    ('software development', 'Software Development'),
    ('QA', 'Quality Assurance'),
    ('project management', 'Project Management'),
    ('Product Management', 'Product Management'),
    ('design', 'Design'),
    ('devOps', 'DevOps'),
    ('customer support', 'Customer Support'),
    ('marketing', 'Marketing'),
    ('IT', 'Information Technology')
)

    employee_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee ID'}))
    department = django_filters.ChoiceFilter(choices=DEPARTMENT_OPT)
    
    
    
    class Meta:
        model = EmployeeInfo
        fields = ('employee_id','department')

    def filter_queryset(self, queryset):
        department_info_value = self.data.get('department')
        employee_id_value = self.data.get('employee_id')

        if department_info_value:
            designation_info = DesignationInfo.objects.filter(department=department_info_value).first()
            queryset = queryset.filter(position=designation_info)
        
        if employee_id_value:
            queryset = queryset.filter(employee_id=employee_id_value)
        
        return queryset


class PayrollMonthListFilter(django_filters.FilterSet):
    current_year = datetime.now().year
    year_choices = [(year, year) for year in range(current_year-5, current_year+5)]
    year = django_filters.ChoiceFilter(choices=year_choices, empty_label='Year')
    
    class Meta:
       model= PayrollMonth
       fields = {
            'month' : {'exact'},
            'year'  : {'exact'}
       }

class LeaveApplicationFilter(django_filters.FilterSet):
    leave_from = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LeaveApplication
        fields = ('leave_from','approved_status')