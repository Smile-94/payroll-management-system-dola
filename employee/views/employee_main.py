from django.urls import reverse_lazy
from django.contrib import messages

# premission classs
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# Generic Views
from django.views.generic import TemplateView
from datetime import datetime

from authority.models import PayrollMonth
from authority.models import LeaveApplication
from authority.models import MonthlyPermitedLeave
from authority.models import PermitedSortLeave
from authority.models import OfficeTime
from authority.models import WeeklyOffday
from authority.models import PermitedLatePresent
from reciption.models import Attendance
from reciption.models import SortLeave


class EmployeeHomeView(LoginRequiredMixin, EmployeePassesTestMixin, TemplateView):
    template_name = 'employee/employee.html'

    def get_context_data(self, **kwargs):
        try:
            current_month_name = datetime.now().strftime('%B')
            current_year_name = datetime.now().strftime('%Y')
            month_obj = PayrollMonth.objects.get(month=current_month_name[0:3], year=current_year_name)
            from_date=month_obj.from_date
            to_date =datetime.today().date()
            this_month_attendance = Attendance.objects.filter(attendance_of=self.request.user.employee_info, date__range=[from_date,to_date]).count()
            total_leave = LeaveApplication.objects.filter(application_of=self.request.user,is_active=True, approved_status=True, leave_from__range=[from_date,to_date]).count()
            permi_late_obje=PermitedLatePresent.objects.last()
            late_present = Attendance.objects.filter(attendance_of=self.request.user.employee_info,date__range=[from_date,to_date], late_present__gt=permi_late_obje.peremited_time).count()

            permited_leave_obj=MonthlyPermitedLeave.objects.get(leave_month=current_month_name[0:3])
            permited_leave_days=permited_leave_obj.permited_days
            permited_late_present = permi_late_obje.permited_days

            permited_sort_leave_obj= PermitedSortLeave.objects.last()
            sort_leave = SortLeave.objects.filter(ticket_for=self.request.user.employee_info, date__range=[from_date,to_date]).count()
            permited_sort_leave = permited_sort_leave_obj.permited_days
            office_time_obj = OfficeTime.objects.last()
            start_time = office_time_obj.office_start
            end_time = office_time_obj.office_end

            weekly_offday_obj=WeeklyOffday.objects.last()
            day1=weekly_offday_obj.first_day
            day2=weekly_offday_obj.second_day

            

        except Exception as e:
            print(e)

        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Home"
        context["total_attendance"] = this_month_attendance 
        context["current_month"] = f"{(current_month_name)[0:3]},{current_year_name}"
        context["leave"] = total_leave
        context["leave_permited"] = permited_leave_days
        context["late"] = late_present
        context["late_permited"] = permited_late_present
        context["half_day"] = sort_leave
        context["half_day_permited"] = permited_sort_leave
        context["office_start"] = start_time
        context["office_end"] = end_time
        context["off_day1"] = day1
        context["off_day2"] = day2

        return context
    