
#Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# Django Generic classes
from django.views.generic import ListView
from django.views.generic import DetailView

# Models
from authority.models import MonthlyPermitedLeave
from authority.models import PermitedLatePresent
from authority.models import PermitedSortLeave
from authority.models import MonthlyHoliday
from authority.models import Notice

# Filters
from authority.filters import MonthlyHolidayFilter
from authority.filters import NoticeFilter


class EmployeePermitedLeaveView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = MonthlyPermitedLeave
    template_name = 'employee/permited_leave_employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Monthly Permited Leave' 
        context["months"] = MonthlyPermitedLeave.objects.filter(is_active=True) 
        return context

class EmployeePermitedLatePresentView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = PermitedLatePresent
    queryset = PermitedLatePresent.objects.filter(is_active=True).order_by('-id')
    template_name = 'employee/employee_permited_late_present.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Late Present'
        context["presents"] = self.queryset
        return context

class EmployeePermitedSortleaveView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = PermitedSortLeave
    queryset = PermitedSortLeave.objects.filter(is_active=True).order_by('-id')
    template_name = 'employee/employee_permited_sort_leave.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Sort Leave'
        context["sortleaves"] = self.queryset
        return context

class EmployeeMonthlyHolidayView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = MonthlyHoliday
    queryset = MonthlyHoliday.objects.filter(is_active= True)
    filterset_class = MonthlyHolidayFilter
    template_name = 'employee/employee_monthly_holyday.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Holiday"
        context["holidays"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

class EmployeeNoticeView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = Notice
    queryset = Notice.objects.filter(is_active= True)
    filterset_class = NoticeFilter
    form_class = NoticeFilter
    template_name = 'employee/employee_notice_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Off Day"
        context["notices"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

class EmployeeNoticeDetailsView(LoginRequiredMixin, EmployeePassesTestMixin, DetailView):
    model = Notice
    context_object_name = 'notice'
    template_name = 'employee/employee_notice_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notice Details"
        return context
  

    
    


