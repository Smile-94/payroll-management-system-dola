
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
from authority.models import OfficeTime
from authority.models import WeeklyOffday


# Create your views here.
class ReceptionView(LoginRequiredMixin, TemplateView):
    template_name = 'reception/reception.html'

    def get_context_data(self, **kwargs):
        try:
            total_employee = EmployeeInfo.objects.all().count()
            today = date.today()
            attend_today = Attendance.objects.filter(date=today).count()
            office_time_obj = OfficeTime.objects.last()
            start_time = office_time_obj.office_start
            end_time = office_time_obj.office_end

            weekly_offday_obj=WeeklyOffday.objects.last()
            day1=weekly_offday_obj.first_day
            day2=weekly_offday_obj.second_day

        except Exception as e:
            print(e)

        context = super().get_context_data(**kwargs)
        context["title"] = "Receptionist Home"
        context["total_employee"] = total_employee
        context["attend_today"] = attend_today
        context["absence_today"] = (total_employee-attend_today)
        context["Sort_leave"] = SortLeave.objects.filter(date=date.today()).count()
        context["late_present"] = Attendance.objects.filter(date=date.today(),late_present__gt=timedelta(minutes=30)).count()
        context["office_start"] = start_time
        context["office_end"] = end_time
        context["off_day1"] = day1
        context["off_day2"] = day2

        return context