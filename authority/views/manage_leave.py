from django.urls import reverse_lazy
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect


# Django Generic View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin

# Models
from authority.models import LeaveApplication

# Forms
from authority.forms import LeavApplicationAcceptForm
from authority.forms import LeaveApplicationRejectForm

# Filters
from authority.filters import LeaveApplicationAuthorityFilter



class LeaveApplicationListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = LeaveApplication
    queryset = LeaveApplication.objects.filter(is_active=True, approved_status=False, declined_status=False)
    filterset_class = LeaveApplicationAuthorityFilter
    template_name = 'authority/leave_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Application List"
        context["leaves"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

class LeaveApplicationDetailsView(LoginRequiredMixin, AdminPassesTestMixin, DetailView):
    model = LeaveApplication
    context_object_name = 'leave'
    form_class = LeavApplicationAcceptForm
    form_class2 = LeaveApplicationRejectForm
    template_name = 'authority/leave_application_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Application Details"
        context["form"] = self.form_class(instance=self.object)
        context["form2"] = self.form_class2(instance=self.object)
        return context

class LeaveApplicationAcceptView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = LeaveApplication
    form_class = LeavApplicationAcceptForm
    template_name = 'authority/leaveapplication_form.html'
    success_url = reverse_lazy('authority:leave_application_details', kwargs={'pk': 0})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Accept"
        return context

    def form_valid(self, form):
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.approvied_by=self.request.user
            form_obj.approved_status = True
            form_obj.save()

        messages.success(self.request, 'leave application accepted')
        self.success_url = reverse_lazy('authority:leave_application_details', kwargs={'pk': self.object.id})
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something wrong please try again!")
        return super().form_invalid(form)


class LeaveApplicationRejectView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveApplicationRejectForm
    template_name = 'authority/leaveapplication_form.html'
    success_url = reverse_lazy('authority:leave_application_details', kwargs={'pk': 0})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reject Application"
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.approvied_by=self.request.user
            form_obj.declined_status = True
            form_obj.save()

        messages.warning(self.request, 'Leave application rejected')
        self.success_url = reverse_lazy('authority:leave_application_details', kwargs={'pk': self.object.id})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Some thing worng please try again")
        return super().form_invalid(form)
    

class LeaveApplicationAcceptedListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = LeaveApplication
    queryset = LeaveApplication.objects.filter(is_active=True, approved_status=True)
    filterset_class = LeaveApplicationAuthorityFilter
    template_name = 'authority/accept_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Accepted Application List"
        context["leaves"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context
    
    
class LeaveApplicationRjectedListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = LeaveApplication
    queryset = LeaveApplication.objects.filter(is_active=True, declined_status=True)
    filterset_class = LeaveApplicationAuthorityFilter
    template_name = 'authority/reject_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Rejected Application List"
        context["leaves"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

class LeaveApplicationDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= LeaveApplication
    context_object_name ='leave'
    template_name = "authority/delete_leave_application.html"
    success_url = reverse_lazy('authority:calculated_salary_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Calculated Salary" 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()

        if self.object.approved_status is True:
            self.success_url = reverse_lazy('authority:accepted_leave_application')

        elif self.object.declined_status is True:
            self.success_url = reverse_lazy('authority:reject_leave_application')
        
        return redirect(self.success_url)


    

    
    

    




