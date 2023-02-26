from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages



# Filters Class
from authority.filters import PayrollMonthListFilter
from authority.filters import MonthlyOffdayListFilter
from authority.filters import MonthlyHolidayFilter


# class-based view classes
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin


# Models Authority
from authority.models import PayrollMonth
from authority.models import FestivalBonus
from authority.models import MonthlyOffDay
from authority.models import MonthlyHoliday


# forms 
from authority.forms import PayrollMonthForm
from authority.forms import FestivalBonusForm
from authority.forms import MonthlyOffDayForm
from authority.forms import MonthlyHolidayForm


class AddPayrollMonthView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = PayrollMonth
    queryset =PayrollMonth.objects.filter(active_status=True).order_by('-id')
    form_class = PayrollMonthForm
    filterset_class = PayrollMonthListFilter
    template_name = 'authority/payroll_month.html'
    success_url = reverse_lazy('authority:add_payrollmonth')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Payroll Month"
        context["months"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context
    
    
    def form_valid(self, form):
        month_value = form.cleaned_data.get('month')
        year_value = form.cleaned_data.get('year')

        if PayrollMonth.objects.filter(month=month_value, year=year_value, active_status=True).exists():
            messages.warning(self.request, f"{month_value},{year_value} already added")
            return redirect(self.success_url)
        
        messages.success(self.request, "Payroll Month Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again")
        return super().form_invalid(form)

class UpdatePayrollMonthView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model=PayrollMonth
    form_class=PayrollMonthForm
    template_name='authority/payroll_month.html'
    success_url= reverse_lazy('authority:add_payrollmonth')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Payroll Month"
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Payroll Month Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong payroll month not updated")
        return super().form_invalid(form)

class DeletePayrollMonthView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= PayrollMonth
    template_name = "authority/delete_payrollmonth.html"
    success_url = reverse_lazy('authority:payrollmonth_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Payroll Month" 
        return context

    def form_valid(self, form):
        self.object.active_status = False
        self.object.save()
        return redirect(self.success_url)

# Monthly offday add,update,delete
class AddMonthlyOffDayView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = MonthlyOffDay
    queryset = MonthlyOffDay.objects.filter(is_active= True)
    filterset_class = MonthlyOffdayListFilter
    form_class = MonthlyOffDayForm
    template_name = 'authority/add_offday.html'
    success_url = reverse_lazy('authority:add_offday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Off Day"
        context["offdays"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

    def form_valid(self, form):
        month_value = form.cleaned_data.get('month')

        if MonthlyOffDay.objects.filter(month=month_value,is_active=True).exists():
            messages.error(self.request, "Month already added")
            return redirect(self.success_url)
        
        messages.success(self.request, "Offday Month added successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Something Went Worng please try again")
        return super().form_invalid(form)
    

class UpdateMonthlyOffdayView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = MonthlyOffDay
    form_class = MonthlyOffDayForm
    template_name = 'authority/add_offday.html'
    success_url = reverse_lazy('authority:add_offday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Monthly Offday"
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Monthly Offday Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Monthly Offday not updated, try again!")
        return super().form_invalid(form)


class DeleteMonthlyOffdayView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= MonthlyOffDay
    template_name = "authority/delete_offday.html"
    success_url = reverse_lazy('authority:add_offday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Offday" 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)
    

class AddMonthlyHoidayView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = MonthlyHoliday
    queryset = MonthlyHoliday.objects.filter(is_active= True)
    filterset_class = MonthlyHolidayFilter
    form_class = MonthlyHolidayForm
    template_name = 'authority/add_holiday.html'
    success_url = reverse_lazy('authority:add_holiday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Holiday"
        context["holidays"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

    def form_valid(self, form):
        date_value = form.cleaned_data.get('holiday_date')

        if MonthlyHoliday.objects.filter(holiday_date=date_value,is_active=True).exists():
            messages.error(self.request, "This holiday already added")
            return redirect(self.success_url)
        
        messages.success(self.request, "Offday Month added successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Something Went Worng please try again")
        return super().form_invalid(form)


class UpdateMonthlyHolidayView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = MonthlyHoliday
    form_class = MonthlyHolidayForm
    template_name =  'authority/add_holiday.html'
    success_url = reverse_lazy('authority:add_holiday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Monthly Holiday'
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Monthly Holiday Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Monthly Holiday not updated, try again!")
        return super().form_invalid(form)


class DeleteMonthlyHolidayView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= MonthlyHoliday
    template_name = "authority/delete_holiday.html"
    success_url = reverse_lazy('authority:add_holiday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Holiday" 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)

    

# Festival Bonus add,update, delete

class FestivalBonusView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = FestivalBonus
    form_class = FestivalBonusForm
    template_name='authority/festival_bonus.html'
    success_url=reverse_lazy('authority:festival_bonus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Festival Bonus" 
        context["festivals"] = FestivalBonus.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Festival Bonus Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Festival not added try again!")
        return super().form_invalid(form)


class FestivalBonusUpdateView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = FestivalBonus
    form_class = FestivalBonusForm
    template_name = 'authority/festival_bonus.html'
    success_url = reverse_lazy('authority:festival_bonus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Festival Bonus" 
        context["updated"] = True 
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Festival Bonus Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Festival Bonus not updated try again !')
        return super().form_invalid(form)

