from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
import datetime
from datetime import timedelta
from datetime import date

# Permissions Classes
from django.contrib.auth.mixins import LoginRequiredMixin

# filters
from reciption.filters import SortLeaveFilters

# Class based Vieww
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.views.generic import DeleteView

# Models
from employee.models import EmployeeInfo
from reciption.models import SortLeave

# forms
from reciption.forms import SortLeaveForm


class AddSortleaveView(CreateView):
    model = SortLeave
    form_class = SortLeaveForm
    template_name = 'reception/add_sortleave.html'
    success_url = reverse_lazy('reception:sortleave_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Issue Sort Leave" 
        return context
    
    def form_valid(self, form):
        employee_id = form.cleaned_data['employee_id']
        today = date.today()

        try:
            employee_info = EmployeeInfo.objects.get(employee_id=employee_id)

            leave_obj = SortLeave.objects.filter(date=today, employee_id=employee_id, active_status=True).exists()

            if leave_obj is True:
                messages.error(self.request, "Employee have already issued a leave")
                return self.form_invalid(form)
            
            if form.is_valid():
                form_obj = form.save(commit=False)
                form_obj.ticket_for = employee_info
                form_obj.issued_by = self.request.user
                form_obj.save()
                messages.success(self.request, "Sort Leave added successfully")

            return super().form_valid(form)

        except Exception as e:
            print(e)
            messages.error(self.request, "Somethin went worng try again")
            return self.form_invalid(form)


class SortleaveListView(LoginRequiredMixin, ListView):
    queryset = SortLeave.objects.filter(active_status=True).order_by('-id')
    filterset_class = SortLeaveFilters
    template_name = "reception/sortleave_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sortleave List" 
        context["leaves"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context


class SortLeaveDetailView(DetailView):
    model = SortLeave
    context_object_name = 'leave'
    template_name = 'reception/sortleave_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sortleave Detail" 
        return context


class SortLeaveUpdateView(LoginRequiredMixin, UpdateView):
    model = SortLeave
    form_class = SortLeaveForm
    template_name = 'reception/update_sortleave.html'
    success_url = reverse_lazy('reception:sortleave_list')

    def get_context_data(self, **kwargs):
        update_info = SortLeave.objects.get(id=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Sortleave"
        context["form"] = self.form_class(instance=update_info)
        return context
    
    def post(self, request, *args, **kwargs):
        update_info = SortLeave.objects.get(id=self.kwargs.get('pk'))
        form = self.form_class(request.POST, instance=update_info)
        return self.form_valid(form)
    
    def form_valid(self, form):
        try:
            if form.is_valid():
                outing_time=form.cleaned_data['outing_time']
                entry_time=form.cleaned_data['entering_time']
                leave_hour=form.cleaned_data['leave_hour']

                outing=datetime.datetime.combine(datetime.date.today(), outing_time)
                entering=datetime.datetime.combine(datetime.date.today(), entry_time)
                late_entry=((entering-outing)-leave_hour)
                form_obj=form.save(commit=False)
                if late_entry > timedelta(seconds=0):
                    form_obj.late_entry = late_entry
                else:
                    form_obj.late_entry = timedelta(seconds=0)
                form_obj.save()
                messages.success(self.request, "Leave Updated Successfully")
            return super().form_valid(form)

        except Exception as e:
            print(e)
            return self.form_invalid(form)

class SortleaveDeleteView(DeleteView):
    model=SortLeave
    context_object_name='leave'
    template_name="reception/delete_sortleave.html"
    success_url=reverse_lazy('reception:sortleave_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Sort Leave"
        return context
    

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.active_status = False
        self.object.save()
        messages.success(self.request, "delete sortleave successfully")
        return redirect(success_url)