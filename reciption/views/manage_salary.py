
# Generic Classes
from django.views.generic import ListView
from django.views.generic import DetailView


# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from reciption.permissions import ReceptionPassesTestMixin

# Models
from employee.models import MonthlySalary


class RecptionMonthlySalaryListView(LoginRequiredMixin, ReceptionPassesTestMixin, ListView):
    model = MonthlySalary
    template_name = 'reception/reception_salary_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Salary List" 
        context["salarys"] = MonthlySalary.objects.filter(is_active=True,salary_employee=self.request.user.employee_info ).order_by('-id')
        return context

class ReceptionMonthlySalaryDetailsView(LoginRequiredMixin, ReceptionPassesTestMixin, DetailView):
    model = MonthlySalary
    context_object_name = 'salary'
    template_name = 'reception/reception_salary_details.html'

    def get_context_data(self, **kwargs):
        query_obj = self.get_object()
        total_salary = query_obj.total_salary
        total_diduct = query_obj.total_diduct
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Salary Details" 
        context["total_salary_pay"] =round(total_salary-total_diduct)
        return context
    