from django.urls import reverse_lazy


# Django Generic View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView

# Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin

# Models
from authority.models import LeaveApplication

# Forms
from authority.forms import LeavApplicationAcceptForm

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
    template_name = 'authority/leave_application_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Application Details"
        context["form"] = self.form_class(instance=self.object)
        return context

class LeaveApplicationAcceptView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = LeaveApplication
    form_class = LeavApplicationAcceptForm
    success_url = reverse_lazy('authority:leave_application_details', kwargs={'pk': 0})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Accept" 
        return context

    def form_valid(self, form):

        self.success_url = reverse_lazy('authority:leave_application_details', kwargs={'pk': self.object.id})
        return super().form_valid(form)
    
    

    




