from django.urls import reverse_lazy
from django.contrib import messages

# Generic Views
from django.views.generic import TemplateView



class EmployeeHomeView(TemplateView):
    template_name = 'employee/employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Home" 
        return context
    