from django.urls import reverse_lazy
from django.contrib import messages

# premissions class
from django.contrib.auth.mixins import LoginRequiredMixin
from reciption.permissions import ReceptionPassesTestMixin

# filters
from authority.filters import LeaveApplicationFilter

# Import Generic Views
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView

# Models
from authority.models import LeaveApplication

# Forms
from authority.forms import LeaveApplicationForm


class AddLeaveApplicationView(LoginRequiredMixin, ReceptionPassesTestMixin, CreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    queryset= LeaveApplication.objects.filter(is_active=True).order_by('-id')
    filterset_class = LeaveApplicationFilter
    template_name = 'reception/leave_application.html'
    success_url = reverse_lazy('employee:apply_leave')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(application_of=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Application"
        context["leaves"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
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

class LeaveApplicationUpdateView(LoginRequiredMixin,ReceptionPassesTestMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = 'reception/leave_application.html'
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

class LeaveApplicationDetailsView(LoginRequiredMixin, ReceptionPassesTestMixin, DetailView):
    model = LeaveApplication
    context_object_name = 'leave'
    template_name = 'reception/leave_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Details"
        return context