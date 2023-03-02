
from datetime import timedelta
from datetime import date

# Permissions Classes
from django.contrib.auth.mixins import LoginRequiredMixin

# Class based View
from django.views.generic import TemplateView


# Models
from employee.models import EmployeeInfo
from reciption.models import Attendance
from reciption.models import SortLeave


# Create your views here.
class ReceptionView(LoginRequiredMixin, TemplateView):
    template_name = 'reception/reception.html'

    def get_context_data(self, **kwargs):
        total_employee = EmployeeInfo.objects.all().count()
        today = date.today()
        attend_today = Attendance.objects.filter(date=today).count()
        context = super().get_context_data(**kwargs)
        context["title"] = "Receptionist Home"
        
        context["total_employee"] = total_employee
        context["attend_today"] = attend_today
        context["absence_today"] = (total_employee-attend_today)
        context["Sort_leave"] = SortLeave.objects.filter(date=date.today()).count()
        context["late_present"] = Attendance.objects.filter(date=date.today(),late_present__gt=timedelta(minutes=30)).count()

        return context