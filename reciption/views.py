from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import date

# Permissions Classes
from django.contrib.auth.mixins import LoginRequiredMixin

# filters
from reciption.filters import AttendanceFilters
from reciption.filters import SortLeaveFilters

# Class based View
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DetailView

# Models
from employee.models import EmployeeInfo
from reciption.models import Attendance
from reciption.models import SortLeave

# forms
from reciption.forms import AttendanceForm
from reciption.forms import SortLeaveForm

# Create your views here.
class ReceptionView(LoginRequiredMixin,TemplateView):
    template_name='reception/reception.html'

    
    def get_context_data(self, **kwargs):
        total_employee=EmployeeInfo.objects.all().count()
        today=date.today()
        attend_today=Attendance.objects.filter(date=today).count()
        context = super().get_context_data(**kwargs)
        context["title"] = "Receptionnis Home"
        
        context["total_employee"] = total_employee
        context["attend_today"] = attend_today
        context["absence_today"] = (total_employee-attend_today)
        context["Sort_leave"] = SortLeave.objects.filter(date=date.today()).count()

        return context

class AddAttendanceView(LoginRequiredMixin, CreateView):
    model= Attendance
    form_class=AttendanceForm
    template_name='reception/add_attendance.html'
    success_url=reverse_lazy('reception:add_attendance')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Attendance" 
        return context

    def form_valid(self, form):
        employee_id= form.cleaned_data['employee_id']
        today=date.today()
        try:
            employee_info=EmployeeInfo.objects.get(employee_id=employee_id)

            if Attendance.objects.filter(date=today, employee_id=employee_id).exists():
                messages.error(self.request, "Employee Attendance already done today")
                return self.form_invalid(form)

            if form.is_valid():
                attendance=form.save(commit=False)
                attendance.attendance_of=employee_info
                attendance.save()

            messages.success(self.request, "Attendance Added Successfully")  
            return super().form_valid(form)

        except Exception as e:
            print(e)
            messages.error(self.request, "Something worng try again")
            return self.form_invalid(form)

class AttendanceListView(ListView):
    model=Attendance
    queryset=Attendance.objects.all().order_by('-pk')
    filterset_class= AttendanceFilters
    template_name='reception/attendance_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Attendance List" 
        context["attendances"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context


class IssuSortLeaveView(CreateView):
    model=SortLeave
    form_class=SortLeaveForm
    template_name='reception/add_sortleave.html'
    success_url=reverse_lazy('reception:reception_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Issue Sortleave" 
        return context
    
    def form_valid(self, form):
        employee_id= form.cleaned_data['employee_id']
        today=today=date.today()
        try:
            employee_info=EmployeeInfo.objects.get(employee_id=employee_id)

            leave_exist=SortLeave.objects.filter(date=today, employee_id=employee_id).exists()

            if leave_exist is True:
                messages.error(self.request, "Already Issued a Sortleave Today")
                return self.form_invalid(form)

            if form.is_valid():
                sort_leave=form.save(commit=False)
                sort_leave.ticket_for=employee_info
                sort_leave.issued_by=self.request.user
                sort_leave.save()
                messages.success(self.request, "Sort leave iccued successfully")

            return super().form_valid(form)

        except Exception as e:
            print(e)
            messages.error(self.request, 'Something goes wrong try again')
            return self.form_invalid(form)

class SortleaveListView(ListView):
    queryset=SortLeave.objects.filter(active_status=True)
    filterset_class = SortLeaveFilters
    template_name="reception/sortleave_list.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sortleave List" 
        context["leaves"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

class SortLeaveDetailView(DetailView):
    model=SortLeave
    template_name = 'reception/sortleave_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sortleave Detail" 
        return context
    

class SortLeaveUpdateView(UpdateView):
    model= SortLeave
    form_class= SortLeaveForm
    template_name='reception/update_sortleave.html' 
    success_url=reverse_lazy('reception:sortleave_list') 

    def get_context_data(self, **kwargs):
        update_info=SortLeave.objects.get(id=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Sortleave"
        context["form"] = self.form_class(instance=update_info)
        return context
    
    def post(self, request, *args, **kwargs):
        update_info=SortLeave.objects.get(id=self.kwargs.get('pk'))
        form= self.form_class(request.POST, instance=update_info)
        return self.form_valid(form)
    
    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.success(self.request, "Leave Updated Successfully")
        return super().form_valid(form)
      
    
        
    
    
        
    
    
            

    
    
