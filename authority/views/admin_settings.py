from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

# permission classes
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin

# Filters Class
from employee.filters import DesignationInfoFilter


# class-based view classes
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


# Models Employee
from employee.models import DesignationInfo

# Models Authority
from authority.models import OfficeTime
from authority.models import MonthlyPermitedLeave
from authority.models import PermitedLatePresent
from authority.models import PermitedSortLeave
from authority.models import WeeklyOffday


# forms 
from employee.forms import DesignationInfoForm
from authority.forms import OfficeTimeForm
from authority.forms import MonthlyPermitedLeaveForm
from authority.forms import PermitedLatePresentForm
from authority.forms import PermitedSortLeaveForm
from authority.forms import WeeklyOffdayForm


class AddDesignationView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = DesignationInfo
    queryset= DesignationInfo.objects.filter(is_active=True)
    form_class = DesignationInfoForm
    filterset_class = DesignationInfoFilter
    template_name = 'authority/add_designation.html'
    success_url = reverse_lazy('authority:add_designation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Designation'
        context["designations"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Designation Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong please try again")
        return super().form_invalid(form)


class DesignationUpdateView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = DesignationInfo
    fields = ('designation', 'department', 'description')
    template_name = 'authority/add_designation.html'
    success_url = reverse_lazy('authority:add_designation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Designation" 
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Designation Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "some thing went wrong try again")
        return super().form_invalid(form)


class DesignationDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = DesignationInfo
    template_name = 'authority/delete_designation.html'
    context_object_name = 'designation'
    success_url = reverse_lazy('authority:add_designation')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return redirect(success_url)

class AddOfficeTimeView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model=OfficeTime
    form_class=OfficeTimeForm
    template_name= "authority/add_office_time.html"
    success_url=reverse_lazy('authority:add_office')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Office Time" 
        context["office_time"] = OfficeTime.objects.all()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Office Time added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Office time not added try again")
        return super().form_invalid(form)


class UpdateOfficeTimeView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model=OfficeTime
    form_class=OfficeTimeForm
    template_name= "authority/add_office_time.html"
    success_url=reverse_lazy('authority:add_officetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Office Time" 
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Office Time added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Office time not added try again")
        return super().form_invalid(form)

class AddPermitedLeaveView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = MonthlyPermitedLeave
    form_class = MonthlyPermitedLeaveForm
    template_name = 'authority/permited_leave.html'
    success_url = reverse_lazy('authority:add_permited_leave')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Monthly Permited Leave' 
        context["months"] = MonthlyPermitedLeave.objects.filter(is_active=True) 
        return context
    
    def form_valid(self, form):
        month = form.cleaned_data.get('leave_month')

        if MonthlyPermitedLeave.objects.filter(leave_month=month).exists():
            messages.warning(self.request, f"{month} already added in the list")
            return redirect(self.success_url)
        
        messages.success(self.request, "Premited Leave added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)

class UpdateMonthlyPermitedLeaveView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = MonthlyPermitedLeave
    form_class = MonthlyPermitedLeaveForm
    template_name = template_name = 'authority/permited_leave.html'
    success_url = reverse_lazy('authority:add_permited_leave')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Monthly Permited Leave" 
        context["updated"] = True 
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.kwargs.get(self.pk_url_kwarg):
            form.fields.get('leave_month').widget.attrs['disabled'] = True
        return form
    
    def form_valid(self, form):
        messages.success(self.request, "Premited Leave added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Monthly Permited leave not updated try again!")
        return super().form_invalid(form)

class DeleteMonthlyPermitedLeaveView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = MonthlyPermitedLeave
    template_name = 'authority/delete_permitedleave.html'
    context_object_name = 'months'
    success_url = reverse_lazy('authority:add_permited_leave')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return redirect(success_url)

class AddPermitedLatePresentView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = PermitedLatePresent
    queryset = PermitedLatePresent.objects.filter(is_active=True).order_by('-id')
    form_class = PermitedLatePresentForm
    template_name = 'authority/permited_latepresent.html'
    success_url = reverse_lazy('authority:add_permited_latepresent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Late Present'
        context["presents"] = self.queryset
        return context
    
    def form_valid(self, form):
        
        messages.success(self.request, "Premited Late Present added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)
    
class UpdatePermitedLatePresentView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = PermitedLatePresent
    form_class = PermitedLatePresentForm
    template_name = 'authority/permited_latepresent.html'
    success_url = reverse_lazy('authority:add_permited_latepresent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Late Present'
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        
        messages.success(self.request, "Premited Late Present Updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)

class DeletePermitedLatePresentView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = PermitedLatePresent
    template_name = 'authority/delete_permitedlatepresent.html'
    context_object_name = 'present'
    success_url = reverse_lazy('authority:add_permited_latepresent')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return redirect(success_url)
    
class AddPermitedSortLeaveView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = PermitedSortLeave
    queryset = PermitedSortLeave.objects.filter(is_active=True).order_by('-id')
    form_class = PermitedSortLeaveForm
    template_name = 'authority/permited_sortleave.html'
    success_url = reverse_lazy('authority:add_permited_sortleave')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Sort Leave'
        context["sortleaves"] = self.queryset
        return context
    
    def form_valid(self, form):
        
        messages.success(self.request, "Premited Sort Leave added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)
    
class UpdatePermitedSortLeaveView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = PermitedSortLeave
    form_class = PermitedSortLeaveForm
    template_name = 'authority/permited_sortleave.html'
    success_url = reverse_lazy('authority:add_permited_sortleave')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Sort Leave'
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        
        messages.success(self.request, "Premited Sort Leave Updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)

class DeletePermitedSortLeaveView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = PermitedSortLeave
    template_name = 'authority/delete_permited_sortleave.html'
    context_object_name = 'sortleave'
    success_url = reverse_lazy('authority:add_permited_sortleave')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return redirect(success_url)

class AddWeeklyOffDayView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = WeeklyOffday
    form_class = WeeklyOffdayForm
    template_name = 'authority/weekly_offday.html'
    success_url = reverse_lazy('authority:add_weekly_offday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Weekly off day'
        context["offdays"] = WeeklyOffday.objects.filter(is_active=True).order_by('-id')
        return context
    
    def form_valid(self, form):
        
        messages.success(self.request, "Weekly off day added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)

class UpdateWeeklyOffdayView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = WeeklyOffday
    form_class = WeeklyOffdayForm
    template_name = 'authority/weekly_offday.html'
    success_url = reverse_lazy('authority:add_weekly_offday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Sort Leave'
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        
        messages.success(self.request, "Weekly off Day Updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)

class DeleteWeeklyOffdayView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = WeeklyOffday
    template_name = 'authority/delete_weekly_offday.html'
    context_object_name = 'offday'
    success_url = reverse_lazy('authority:add_weekly_offday')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return redirect(success_url)


    
    