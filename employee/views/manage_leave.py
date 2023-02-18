from django.urls import reverse_lazy
from django.contrib import messages

# premissions class
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# filters
from authority.filters import LeaveApplicationFilter

# Import Generic Views
from django.views.generic import CreateView
from django.views.generic import UpdateView

# Models
from authority.models import LeaveApplication

# Forms
from authority.forms import LeaveApplicationForm


class AddLeaveApplicationView(LoginRequiredMixin,EmployeePassesTestMixin, CreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    queryset= LeaveApplication.objects.filter(is_active=True)
    filterset_class = LeaveApplicationFilter
    template_name = 'employee/leave_application.html'
    success_url = reverse_lazy('employee:apply_leave')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Application"
        context["leaves"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

    def form_valid(self, form):
        if form.is_valid():
            leave_form=form.save(commit=False)
            leave_form.application_of= self.request.user
            leave_form.save()
        messages.success(self.request, "Applied Leave application successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Leave Application not Applied successfully try again")
        return super().form_invalid(form)

class LeaveApplicationUpdateView(LoginRequiredMixin,EmployeePassesTestMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = 'employee/leave_application.html'
    success_url = reverse_lazy('employee:apply_leave')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Leave Application" 
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Leave Application Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "some thing went wrong try again")
        return super().form_invalid(form)