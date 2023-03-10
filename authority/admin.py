from django.contrib import admin

# models
from authority.models import OfficeTime
from authority.models import PayrollMonth
from authority.models import MonthlyOffDay
from authority.models import MonthlyHoliday
from authority.models import FestivalBonus
from authority.models import MonthlyPermitedLeave
from authority.models import LeaveApplication
from authority.models import PermitedLatePresent
from authority.models import PermitedSortLeave
from authority.models import WeeklyOffday
from authority.models import Notice


# Register your models here.
@admin.register(PayrollMonth)
class PayrollMonthAdmin(admin.ModelAdmin):
    list_display = ('month','year','from_date','to_date')
    list_filter = ('month',)
    list_per_page= 50

@admin.register(MonthlyOffDay)
class MonthlyOffDayAdmin(admin.ModelAdmin):
    list_display = ('month','total_offday')

@admin.register(MonthlyHoliday)
class MonthlyHolidayAdmin(admin.ModelAdmin):
    list_display=('holiday_month','holiday_name','holiday_date')

@admin.register(FestivalBonus)
class FestivalBonusAdmin(admin.ModelAdmin):
    list_display=('festival_name','bonus_percentage','created_at','modified_at')

@admin.register(OfficeTime)
class SetOfficeTimeAdmin(admin.ModelAdmin):
    list_display = ('office_start', 'office_end', 'modified_at', 'created_at')

@admin.register(MonthlyPermitedLeave)
class MonthlyPermitedLeaveAdmin(admin.ModelAdmin):
    list_display = ('leave_month','permited_days','salary_diduction','modified_at')
    search_fields = ('leave_month',)
    list_per_page = 50

@admin.register(LeaveApplication)
class LeaveApplication(admin.ModelAdmin):
    list_display=('application_of','approvied_by','leave_from','leave_to','approved_status')


@admin.register(PermitedLatePresent)
class PermitedLatePresentAdmin(admin.ModelAdmin):
    list_display = ('peremited_time', 'permited_days','salary_diduction',)

@admin.register(PermitedSortLeave)
class PermitedSortLeaveAdmin(admin.ModelAdmin):
    list_display = ('permited_days','salary_diduction',)

@admin.register(WeeklyOffday)
class WeeklyOffdayAdmin(admin.ModelAdmin):
    list_display = ('first_day','second_day','created_at','modified_at')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('created_by','date','modified_at',)


