from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from datetime import timedelta


# Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin


# Django Generic Views
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Models
from employee.models import EmployeeInfo
from employee.models import EmployeeSalary
from employee.models import MonthlySalary
from employee.models import FestivalBonus
from authority.models import PayrollMonth
from authority.models import MonthlyOffDay
from authority.models import MonthlyHoliday
from authority.models import PermitedLatePresent
from authority.models import MonthlyPermitedLeave
from authority.models import PermitedSortLeave
from reciption.models import Attendance
from reciption.models import SortLeave

# Forms
from employee.forms import MonthlySalaryForm

# Filters
from authority.filters import SalaryEmployeeFilters
from authority.filters import EmployeeMonthlySalaryFilter
from authority.filters import CalculatedMonthlySalaryFilter



class EmployeeSalaryListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):

    model = EmployeeInfo
    queryset = EmployeeInfo.objects.filter(is_active=True)
    filterset_class = SalaryEmployeeFilters
    template_name = 'authority/salary_employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee List"
        context["form"] = MonthlySalaryForm
        context["employees"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

class MonthilySalaryCalculationView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    
    model = MonthlySalary
    form_class = MonthlySalaryForm
    template_name = 'authority/monthily_salary.html'
    success_url = reverse_lazy('authority:monthly_salary_details', kwargs={'pk': 0})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthily Salary Calculation" 
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['other_pk'] = self.kwargs['pk']
        return initial
    
    def form_valid(self, form):
        try:
            salary_month = form.cleaned_data.get('salary_month')

            employee = EmployeeInfo.objects.get(id = self.kwargs['pk'])
            salary = EmployeeSalary.objects.get(salary_of=employee)

            if MonthlySalary.objects.filter(salary_month=salary_month, salary_employee=employee).exists():
                messages.warning(self.request, "Salary already calculated in this month")
                return redirect(self.success_url)
            
            conveyance =float(salary.basic_salary)*float(salary.conveyance/100)
            food_allowance = float(salary.basic_salary)*float(salary.food_allowance/100)
            medical_allowance = float(salary.basic_salary)*float(salary.medical_allowance/100)
            house_rent = float(salary.basic_salary)*float(salary.house_rent/100)
            mobile_allowance = float(salary.basic_salary)* float(salary.mobile_allowance/100)
            
            festival_bonus=0
            if form.cleaned_data.get('festival_bonus') is not None:
                value = form.cleaned_data.get('festival_bonus')
                fastival= FestivalBonus.objects.get(festival_name=value)
                festival_bonus = float(salary.basic_salary)*float(fastival.bonus_percentage/100)
            
            salary_fields= (conveyance,food_allowance,medical_allowance,house_rent,mobile_allowance,festival_bonus)
            total_salary_value =float(salary.basic_salary)+float(sum(salary_fields))

            # Total Salary Diduction 
            month = PayrollMonth.objects.get(month=salary_month.month)
            days = month.total_days
            month_start = month.from_date
            month_end = month.to_date

            print("Totla Days: ",days)
            print(f"Month Start: {month_start}, Month End: {month_end}")
            
            off_day = 0
            if MonthlyOffDay.objects.filter(month=month).exists():
                day = MonthlyOffDay.objects.get(month=month)
                off_day = day.total_offday
            
            print("Off Day: ",off_day)

            holiday = 0
            if MonthlyHoliday.objects.filter(holiday_month=month).exists():
                holiday = MonthlyHoliday.objects.filter(holiday_month=month, is_active=True).count()
            
            
            month_attendance = Attendance.objects.filter(attendance_of= employee , date__range=[month.from_date,month.to_date]).count()
            late_present = Attendance.objects.filter(attendance_of= employee , date__range=[month.from_date,month.to_date], late_present__gt=timedelta(minutes=30)).count()
            late_sort_leave = SortLeave.objects.filter(ticket_for=employee, date__range=[month.from_date,month.to_date]).count()

            print("Totla Late Present: ", late_present)
            
            print("Attendance: ",month_attendance)  
            
            if form.is_valid():
                form_obj = form.save(commit=False)
                form_obj.salary_employee = employee
                form_obj.prepared_by = self.request.user
                form_obj.salary_of = salary
                form_obj.total_conveyance= conveyance
                form_obj.total_food_allowance = food_allowance
                form_obj.total_medical_allowance = medical_allowance
                form_obj.total_house_rent = house_rent
                form_obj.total_mobile_allowance = mobile_allowance
                form_obj.total_bonus =festival_bonus
                form_obj.total_salary = total_salary_value
                form_obj.save()
                messages.success(self.request, "Salary Added Successfully")
                self.object = form_obj
            self.success_url = reverse_lazy('authority:monthly_salary_details', kwargs={'pk': self.object.id})
            
            return super().form_valid(form)
        except Exception as e:
            print(e)
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went worng try aging!")
        return super().form_invalid(form)


class EmployeeMonthlySalaryListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
     model = MonthlySalary
     queryset = MonthlySalary.objects.filter(is_active=True).order_by('-id')
     filterset_class = EmployeeMonthlySalaryFilter
     template_name = 'authority/employee_salary_list.html'

     def get_initial(self):
        initial = super().get_initial()
        initial['other_pk'] = self.kwargs['pk']
        return initial
     
     def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(salary_employee__id=self.kwargs['pk'])
        

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context["title"] = "Employee Salary List" 
         context["employee"] = EmployeeInfo.objects.filter(id=self.kwargs['pk']).first()
         context["salarys"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
         return context
     

class MonthlyCalculatedSalaryListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = MonthlySalary
    queryset = MonthlySalary.objects.filter(is_active=True).order_by('-id')
    filterset_class = CalculatedMonthlySalaryFilter
    template_name = 'authority/calculated_salary_list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context["title"] = "Calculated Salary List"
         context["salarys"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
         return context


class MonthlySalaryDetailsView(LoginRequiredMixin, AdminPassesTestMixin, DetailView):
    model = MonthlySalary
    context_object_name = 'salary'
    template_name = 'authority/salary_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Salary Details" 
        return context

class UpdateCalculatedSalaryView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = MonthlySalary
    form_class = MonthlySalaryForm
    template_name = 'authority/update_calculated_salary.html'
    success_url = reverse_lazy('authority:calculated_salary_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Calculated Salary"
        context["salary"] = MonthlySalary.objects.get(id=self.kwargs['pk']) 
        return context

    def form_valid(self, form):

        calculated_salary=MonthlySalary.objects.get(id=self.kwargs['pk'])
        

        salary = EmployeeSalary.objects.get(salary_of=calculated_salary.salary_employee)
        

        plus_minus_bonus=0
        if form.cleaned_data.get('festival_bonus') is not None:
            value = form.cleaned_data.get('festival_bonus')
            fastival= FestivalBonus.objects.get(festival_name=value)
            plus_minus_bonus =float(salary.basic_salary)*float(fastival.bonus_percentage/100)
            
           
        if form.cleaned_data.get('festival_bonus') is None:
               plus_minus_bonus =  float(calculated_salary.total_bonus)- float(calculated_salary.total_bonus)
               
        
        if form.is_valid():
            form_obj = form.save(commit=False)

            if calculated_salary.festival_bonus is None:
                form_obj.total_bonus = plus_minus_bonus
                form_obj.total_salary = calculated_salary.total_salary+form_obj.total_bonus

            if calculated_salary.festival_bonus is not None:
                form_obj.total_bonus = form_obj.total_bonus-plus_minus_bonus
                form_obj.total_salary =  calculated_salary.total_salary - form_obj.total_bonus

            form_obj.save()
            messages.success(self.request, "Salary Updated Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Salary not updated please try again!")
        return super().form_invalid(form)

class DeleteCalculatedSalaryView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= MonthlySalary
    context_object_name ='salary'
    template_name = "authority/delete_calculated_salary.html"
    success_url = reverse_lazy('authority:calculated_salary_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Calculated Salary" 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)
    
    
     
    
    
     
        
    
    


