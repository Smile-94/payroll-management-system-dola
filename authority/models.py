from django.db import models
from datetime import datetime
import datetime
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

# Models
from accounts.models import User

# Month choces
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

# Create your models here.
class PayrollMonth(models.Model):
    month=models.CharField(max_length=3, choices=MONTH_CHOICES, default='Jan')
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    from_date=models.DateField(auto_now=False, auto_now_add=False)
    to_date=models.DateField(auto_now=False, auto_now_add=False)
    total_days=models.IntegerField(default=0)
    active_status=models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.total_days = (self.to_date - self.from_date).days + 1
        super(PayrollMonth, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.month)+","+str(self.year)

class FestivalBonus(models.Model):
    festival_name=models.CharField(max_length=20, unique=True)
    bonus_percentage= models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.festival_name

class MonthlyOffDay(models.Model):
    month = models.ForeignKey(PayrollMonth,on_delete=models.CASCADE, related_name='off_month')
    total_offday = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(f"{self.month}'s off day")

class MonthlyHoliday(models.Model):
    holiday_month = models.ForeignKey(PayrollMonth, on_delete=models.CASCADE, related_name='holiday_month')
    holiday_name = models.CharField(max_length=100)
    holiday_date = models.DateField(auto_now=False, auto_now_add=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(f"{self.holiday_month}'s holiday")

class MonthlyPermitedLeave(models.Model):
    leave_month = models.CharField(max_length=3, choices=MONTH_CHOICES, default='Jan')
    permited_days = models.PositiveIntegerField()
    salary_diduction = models.DecimalField(max_digits=5, decimal_places=2,default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(f"{self.leave_month}'s Premited Leave")
    

class OfficeTime(models.Model):
    office_start=models.TimeField(auto_now=False, auto_now_add=False)
    office_end=models.TimeField(auto_now=False, auto_now_add=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) :
        return "Office start and end time"


class LeaveApplication(models.Model):
    application_of = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_employee')
    approvied_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_by',blank=True, null=True)
    employee_id = models.CharField(max_length=10,null=True)
    application_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    leave_from = models.DateField(auto_now=False, auto_now_add=False)
    leave_to = models.DateField(auto_now=False, auto_now_add=False)
    leave_description = models.TextField()
    approved_status = models.BooleanField(default=False)
    declined_status = models.BooleanField(default=False)
    declined_message = models.TextField(null=True)
    total_days = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        self.total_days = (self.leave_to - self.leave_from).days + 1
        super(LeaveApplication, self).save(*args, **kwargs)
        if not self.application_id:
            year = str(datetime.date.today().year)[2:4]
            month = str(datetime.date.today().month)
            day = str(datetime.date.today().day)
            self.application_id = 'LA'+year+month+day+str(self.pk).zfill(4)
            self.save()
    
    def __str__(self):
        return str(f"{self.application_of}'s leave application")


class PermitedLatePresent(models.Model):
    peremited_time = models.DurationField()
    permited_days = models.PositiveIntegerField()
    salary_diduction = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str("Permited Late Present")

class PermitedSortLeave(models.Model):
    permited_days = models.PositiveIntegerField()
    salary_diduction = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str("Permited Sort Leave")


class Notice(models.Model):
    subject= models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice_user')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.subject[0:20])

class WeeklyOffday(models.Model):
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    first_day = models.CharField(max_length=13, choices=DAYS_OF_WEEK)
    second_day = models.CharField(max_length=13, choices=DAYS_OF_WEEK, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(f"{self.first_day} off day")




