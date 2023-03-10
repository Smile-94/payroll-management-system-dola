from django.urls import reverse_lazy
from django.contrib import messages

# premissions class
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# filters
from authority.filters import LeaveApplicationFilter
from reciption.filters import SortLeaveFilters

# Import Generic Views
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.views.generic import ListView

# Models
from authority.models import LeaveApplication
from reciption.models import SortLeave


# Forms
from authority.forms import LeaveApplicationForm


class AddLeaveApplicationView(LoginRequiredMixin, EmployeePassesTestMixin, CreateView):
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
            leave_form.employee_id = self.request.user.employee_info.employee_id
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

class LeaveApplicationDetailsView(LoginRequiredMixin, EmployeePassesTestMixin, DetailView):
    model = LeaveApplication
    context_object_name = 'leave'
    template_name = 'employee/leave_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Details"
        return context

class EmployeeSortleaveListView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    queryset = SortLeave.objects.filter(active_status=True).order_by('-id')
    filterset_class = SortLeaveFilters
    template_name = "employee/employee_haflday_leave.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        # Check if form_date or to_date filters are applied
        form_date_filter = self.request.GET.get('from_date', '')
        to_date_filter = self.request.GET.get('to_date', '')
        
        if form_date_filter or to_date_filter:
            # If either filter is applied, switch the ordering to ascending by date
            queryset = queryset.order_by('date')
        else:
            # Otherwise, keep the original ordering by date in descending order
            queryset = queryset.filter(ticket_for=self.request.user.employee_info,).order_by('-id')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sortleave List" 
        context["leaves"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
        return context

class EmployeeSortLeaveDetailView(LoginRequiredMixin, EmployeePassesTestMixin, DetailView):
    model = SortLeave
    context_object_name = 'leave'
    template_name = 'employee/employee_sort_leave_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sortleave Detail" 
        return context

    