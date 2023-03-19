from django.db import models
import datetime

# models
from employee.models import EmployeeInfo
from accounts.models import User
from authority.models import OfficeTime

# Create your models here.
class Attendance(models.Model):
    attendance_of=models.ForeignKey(EmployeeInfo,on_delete=models.CASCADE,related_name='attendance')
    employee_id=models.CharField(max_length=50)
    date=models.DateField(auto_now=False, auto_now_add=False)
    entering_time=models.TimeField(auto_now=False, auto_now_add=False,null=True)
    exit_time=models.TimeField(auto_now=False, auto_now_add=False, null=True)
    late_present = models.DurationField(blank=True, null=True)
    is_active =models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.late_present:
            office_time = OfficeTime.objects.all().first()
            start_time=datetime.datetime.combine(datetime.date.today(), office_time.office_start)
            entry_time=datetime.datetime.combine(datetime.date.today(), self.entering_time)
            self.late_present = (entry_time-start_time)
            self.save()

    def __str__(self):
        return str(self.attendance_of)

class SortLeave(models.Model):
    ticket_for=models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE, related_name='sort_leave')
    issued_by=models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_id=models.CharField(max_length=50)
    employee_id=models.CharField(max_length=50)
    date=models.DateField(auto_now=False, auto_now_add=False)
    outing_time=models.TimeField(auto_now=False, auto_now_add=False)
    description=models.TextField(blank=True)
    active_status=models.BooleanField(default=True)

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.ticket_id:
            month=str(datetime.date.today().month)
            day=str(datetime.date.today().day)
            self.ticket_id = 'TL'+month+day+str(self.pk).zfill(4)
            self.save()

    def __str__(self):
        return str(self.ticket_for)

