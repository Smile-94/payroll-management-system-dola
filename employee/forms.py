from django import forms

#models
from employee.models import DesignationInfo
from employee.models import EmployeeInfo
from employee.models import EmployeeSalary
from employee.models import MonthlySalary

# Custom widgets
from employee.widgets import CustomPictureImageFieldWidget
from employee.widgets import CustomSignetureImageFieldWidget

class EmployeeInfoForm(forms.ModelForm):
    employee_id = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    photo = forms.ImageField(widget=CustomPictureImageFieldWidget)
    signature = forms.ImageField(widget=CustomSignetureImageFieldWidget)

    class Meta:
        model=EmployeeInfo
        exclude=('info_of','is_active')

class EmployeeSalaryForm(forms.ModelForm):

    class Meta:
        model=EmployeeSalary
        exclude=('salary_of',)

class MonthlySalaryForm(forms.ModelForm):

    class Meta:
        model = MonthlySalary
        fields = ('salary_month','festival_bonus',)


class DesignationInfoForm(forms.ModelForm):
    
    class Meta:
        model = DesignationInfo
        exclude = ('is_active',)
