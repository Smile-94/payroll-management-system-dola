from django.db import models
import datetime
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from accounts.models import User
from authority.models import PayrollMonth
from authority.models import FestivalBonus


# utils functions
from employee.utils import user_directory_path


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


class DesignationInfo(models.Model):
    designation = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_OPT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.designation}, {self.department}"


# Create your models here.
class EmployeeInfo(models.Model):
    info_of = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_info')
    position = models.ForeignKey(DesignationInfo, on_delete=models.SET_NULL, blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=15)
    national_id = models.CharField(max_length=50)
    passport_no = models.CharField(max_length=50, blank=True, null=True)
    driving_license = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to=user_directory_path)
    signature = models.ImageField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.employee_id:
            year = str(datetime.date.today().year)[2:4]
            month = str(datetime.date.today().month)
            day = str(datetime.date.today().day)
            self.employee_id = 'E'+year+month+day+str(self.pk).zfill(4)
            self.save()
        
    def __str__(self):
        return str(self.info_of)


class EmployeeSalary(models.Model):
    salary_of = models.OneToOneField(EmployeeInfo, on_delete=models.CASCADE, related_name='salary_info')
    basic_salary = models.PositiveIntegerField(default=0)
    conveyance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    food_allowance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    medical_allowance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    house_rent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    mobile_allowance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return str(self.salary_of)


class MonthlySalary(models.Model):
    salary_employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE, related_name='salary_employee')
    salary_month = models.ForeignKey(PayrollMonth, on_delete=models.CASCADE, related_name='salary_month')
    salary_of = models.ForeignKey(EmployeeSalary, on_delete=models.CASCADE, related_name='base_salary', null=True)
    festival_bonus = models.ForeignKey(FestivalBonus, on_delete=models.CASCADE, related_name='festival_bonus', blank=True, null=True)
    prepared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prepared_by',null=True)
    total_conveyance = models.FloatField()
    total_food_allowance = models.FloatField()
    total_medical_allowance = models.FloatField()
    total_house_rent = models.FloatField()
    total_mobile_allowance = models.FloatField()
    total_bonus = models.FloatField(default=0.0)
    late_present_diduct = models.FloatField(default=0.0)
    sort_leave_diduct = models.FloatField(default=0.0)
    extra_leave_diduct = models.FloatField(default=0.0)
    total_diduct = models.FloatField(null=True)
    total_salary = models.FloatField(null=True)
    total_absence = models.IntegerField(null=True)
    exatra_sort_leave = models.IntegerField(null=True)
    extra_late_present = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.salary_employee)+","+str(self.salary_month)






