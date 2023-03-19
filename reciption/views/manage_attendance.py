from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
import datetime
from datetime import date

# Permissions Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from reciption.permissions import ReceptionPassesTestMixin

# filters
from reciption.filters import AttendanceFilters

# Class based View
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Models
from employee.models import EmployeeInfo
from reciption.models import Attendance

# forms
from reciption.forms import AttendanceForm


class AddAttendanceView(LoginRequiredMixin, ReceptionPassesTestMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'reception/add_attendance.html'
    success_url = reverse_lazy('reception:add_attendance')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Attendance" 
        return context

    def form_valid(self, form):
        employee_id = form.cleaned_data['employee_id']
        attend_date = form.cleaned_data.get('date')
        try:
            employee_info = EmployeeInfo.objects.get(employee_id=employee_id)

            if Attendance.objects.filter(date=attend_date, employee_id=employee_id).exists():
                messages.error(self.request, f"Employee Attendance already done for {attend_date}")
                return self.form_invalid(form)

            if form.is_valid():
                attendance = form.save(commit=False)
                attendance.attendance_of = employee_info
                
                attendance.save()

            messages.success(self.request, "Attendance Added Successfully")  
            return super().form_valid(form)

        except Exception as e:
            print(e)
            messages.error(self.request, "Something worng try again")
            return self.form_invalid(form)

class UpdateAttendaceView(LoginRequiredMixin, ReceptionPassesTestMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'reception/attendance_list.html'
    success_url = reverse_lazy('reception:attendance_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Attendance"
        context["updated"] = True
        return context
    

class AttendanceListView(LoginRequiredMixin, ReceptionPassesTestMixin, ListView):
    model = Attendance
    queryset = Attendance.objects.all().order_by('-date')
    filterset_class = AttendanceFilters
    template_name = 'reception/attendance_list.html'

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
            queryset = queryset.order_by('-date')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Attendance List" 
        context["attendances"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
        return context

class DeleteAttendanceView(LoginRequiredMixin, ReceptionPassesTestMixin, DeleteView):
    model= Attendance
    context_object_name = "attendance"
    template_name = 'reception/attendance_list.html'
    success_url = reverse_lazy('reception:attendance_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Attendance" 
        context["deleted"] = True
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)