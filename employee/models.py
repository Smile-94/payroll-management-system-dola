from django.db import models
import datetime
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from accounts.models import User


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
    designation=models.CharField(max_length=50, unique=True)
    department=models.CharField(max_length=20, choices=DEPARTMENT_OPT)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    description=models.TextField(blank=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.designation}, {self.department}"


# Create your models here.
class EmployeeInfo(models.Model):
    info_of = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_info')
    position = models.ForeignKey(DesignationInfo,on_delete=models.SET_NULL, blank=True, null=True)
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
        prev_id = self.id
        super().save(*args, **kwargs)
        if not self.employee_id:
            year=str(datetime.date.today().year)[2:4]
            month=str(datetime.date.today().month)
            day=str(datetime.date.today().day)
            self.employee_id = 'E'+year+month+day+str(self.pk).zfill(4)
            self.save()
        
    def __str__(self):
        return str(self.info_of)

class EmployeeSalary(models.Model):
    salary_of=models.OneToOneField(EmployeeInfo, on_delete=models.CASCADE, related_name='salary_info')
    basic_salary=models.PositiveIntegerField()
    conveyance=models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    food_allowance=models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    medical_allowance=models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    house_rent=models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    mobile_allowance=models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.salary_of





