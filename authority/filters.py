import django_filters
from django import forms
from datetime import datetime

# models
from accounts.models import User
from employee.models import EmployeeInfo
from employee.models import DesignationInfo
from employee.models import MonthlySalary
from authority.models import PayrollMonth
from authority.models import LeaveApplication
from authority.models import MonthlyOffDay
from authority.models import MonthlyHoliday
from authority.models import Notice


# Global Veriable
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

MONTH_CHOICES = [
        ('Jan', 'January'),
        ('Feb', 'February'),
        ('Mar', 'March'),
        ('Apr', 'April'),
        ('May', 'May'),
        ('Jun', 'June'),
        ('Jul', 'July'),
        ('Aug', 'August'),
        ('Sep', 'September'),
        ('Oct', 'October'),
        ('Nov', 'November'),
        ('Dec', 'December'),
    ]


class EmployeeListFilter(django_filters.FilterSet):

    email = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = {
            'email': {'exact'},
        }


class SalaryEmployeeFilters(django_filters.FilterSet):

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
    

class EmployeeMonthlySalaryFilter(django_filters.FilterSet):
   
    class Meta:
        model = MonthlySalary
        fields =('salary_month', 'festival_bonus')
    
    

class CalculatedMonthlySalaryFilter(django_filters.FilterSet):

    employee_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee ID'}))
   
    class Meta:
        model = MonthlySalary
        fields =( 'employee_id', 'salary_month', 'festival_bonus')
    
    def filter_queryset(self, queryset):
        employee_id_value = self.data.get('employee_id')
        salary_month_value = self.data.get('salary_month')
        festival_bonus_value = self.data.get('festival_bonus')

        if employee_id_value:
            queryset = queryset.filter(salary_employee__employee_id=employee_id_value)
        
        if salary_month_value:
            queryset = queryset.filter(salary_month=salary_month_value)

        if festival_bonus_value:
            queryset = queryset.filter(festival_bonus=festival_bonus_value)
        
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

class MonthlyOffdayListFilter(django_filters.FilterSet):
    
    month = django_filters.ChoiceFilter(choices= MONTH_CHOICES)

    class Meta:
        model = MonthlyOffDay
        fields = ('month',)
    
    def filter_queryset(self, queryset):
        month_value = self.data.get('month')

        if month_value:
            queryset = queryset.filter(month__month=month_value)
        
        return queryset

class MonthlyHolidayFilter(django_filters.FilterSet):

    holiday_month = django_filters.ChoiceFilter(choices= MONTH_CHOICES)
    holiday_name= django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Holiday Name'}))

    class Meta:
        model = MonthlyHoliday
        fields = ('holiday_month','holiday_name')
    
    def filter_queryset(self, queryset):
        month_value = self.data.get('holiday_month')
        name_value = self.data.get('holiday_name')

        if month_value:
            queryset = queryset.filter(holiday_month__month=month_value)
        
        if name_value:
            queryset = queryset.filter(holiday_name__icontains=name_value)
        
        return queryset

class LeaveApplicationFilter(django_filters.FilterSet):
    leave_from = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LeaveApplication
        fields = ('leave_from','approved_status')

class LeaveApplicationAuthorityFilter(django_filters.FilterSet):
    application_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Application ID'}))
    employee_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee ID'}))
    leave_from = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))
    leave_to = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = LeaveApplication
        fields = ('application_id','employee_id',  'leave_from','leave_to')

class NoticeFilter(django_filters.FilterSet):

    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), label='From')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', widget=forms.DateInput(attrs={'type': 'date'}), label='To')
    subject = django_filters.CharFilter(field_name='subject', lookup_expr='icontains', label='Subject', widget=forms.TextInput(attrs={'placeholder': 'Search by subject...'}))

    class Meta:
        model = Notice
        fields = ('subject','date')