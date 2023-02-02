from django.contrib import admin
from employee.models import DesignationInfo
from employee.models import EmployeeInfo
from employee.models import EmployeeSalary

# Register your models here.
class DesignationAdmin(admin.ModelAdmin):
    list_display=('designation','department','created_at','updated_at')
    search_fields=('designation','department')
    list_per_page=50
    
admin.site.register(DesignationInfo)
admin.site.register(EmployeeInfo)
admin.site.register(EmployeeSalary)
