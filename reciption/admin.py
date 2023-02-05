from django.contrib import admin

# Models
from reciption.models import Attendance
from reciption.models import SortLeave

# Register your models here.


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_of', 'employee_id', 'date', 'entering_time', 'exit_time')
    search_fields = ('attendance_of', 'employee_id')
    list_per_page = 50


@admin.register(SortLeave)
class SortLeaveAdmin(admin.ModelAdmin):
    list_display = ('ticket_for', 'issued_by', 'ticket_id', 'employee_id', 'date')
    search_fields = ('ticket_id', 'employee_id')
    list_per_page = 50
