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
from authority.models import PermitedLatePresent
from reciption.models import Attendance


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
            permi_late_obje=PermitedLatePresent.objects.first()
            late_present = Attendance.objects.filter(attendance_of=self.request.user.employee_info,date__range=[from_date,to_date], late_present__gt=permi_late_obje.peremited_time).count()
            print("Late Present: ",late_present)
            # print("Late present: ",late_present)

        except Exception as e:
            print(e)

        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Home"
        context["total_attendance"] = this_month_attendance 
        context["current_month"] = f"{current_month_name},{current_year_name}"
        context["leave"] = total_leave
        context["late"] = late_present

        return context
    