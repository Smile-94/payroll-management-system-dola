from django.urls import reverse_lazy


# Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin


# Django Generic Views
from django.views.generic import ListView

# Models
from employee.models import EmployeeInfo

# Filters
from authority.filters import SalaryEmployeeFilters



class EmployeeSalaryListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):

    model = EmployeeInfo
    queryset = EmployeeInfo.objects.filter(is_active=True)
    filterset_class = SalaryEmployeeFilters
    template_name = 'authority/salary_employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee List"
        context["employees"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context
    


