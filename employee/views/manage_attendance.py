from datetime import datetime

# Permission Classed
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# Generic Classes
from django.views.generic import ListView

# Models
from reciption.models import Attendance


class EmployeeAttedanceListView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = Attendance
    template_name = 'employee/attendance_list.html'


    def get_context_data(self, **kwargs):
        current_month = datetime.today().month
        context = super().get_context_data(**kwargs)
        context["title"] = "My Attendance"
        context["attendances"] = Attendance.objects.filter(is_active=True, attendance_of=self.request.user.employee_info, date__month= current_month)
        return context
    