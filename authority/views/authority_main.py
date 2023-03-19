from django.shortcuts import redirect
from datetime import datetime,timedelta
from datetime import date

from django.db.models import Count, Sum
from django.utils import timezone

# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin

# Generc Classes
from django.views.generic import TemplateView

# Models
from employee.models import EmployeeInfo
from reciption.models import Attendance
from reciption.models import SortLeave
from authority.models import LeaveApplication
from authority.models import OfficeTime




# Create your views here.
class AdminView(LoginRequiredMixin, AdminPassesTestMixin, TemplateView):
    template_name = 'authority/admin.html'
    

    def get_context_data(self, **kwargs):

        total_employee = EmployeeInfo.objects.all().count()
        today = date.today()
        attend_today = Attendance.objects.filter(date=today).count()
        leave_today = LeaveApplication.objects.filter(is_active=True, leave_from=today, approved_status=True).count()
        office_time = OfficeTime.objects.filter(is_active=True).order_by('-id').first()
        context = super().get_context_data(**kwargs)
        context["title"] = "Admin Panel" 
        context["total_employee"] = total_employee
        context["attend_today"] = attend_today
        context["absence_today"] = (total_employee-attend_today-leave_today)
        context["Sort_leave"] = SortLeave.objects.filter(date=date.today()).count()
        context["late_present"] = Attendance.objects.filter(date=date.today(),late_present__gt=timedelta(minutes=30)).count() 
        context["leave_today"] = leave_today
        context["office_time"] = office_time
        return context
