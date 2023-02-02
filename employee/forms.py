from django import forms

#models
from employee.models import DesignationInfo
from employee.models import EmployeeInfo
from employee.models import EmployeeSalary


class DesignationInfoForm(forms.ModelForm):
    
    class Meta:
        model = DesignationInfo
        exclude = ('is_active',)