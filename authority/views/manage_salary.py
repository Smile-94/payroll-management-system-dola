from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


# Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin


# Django Generic Views
from django.views.generic import ListView
from django.views.generic import CreateView

# Models
from employee.models import EmployeeInfo
from employee.models import EmployeeSalary
from employee.models import MonthlySalary
from employee.models import FestivalBonus

# Forms
from employee.forms import MonthlySalaryForm

# Filters
from authority.filters import SalaryEmployeeFilters
from authority.filters import EmployeeMonthlySalaryFilter



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
    success_url = reverse_lazy('authority:salary_employee_list')

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
                print("Exist")
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
                
            
            if form.is_valid():
                form_obj = form.save(commit=False)
                form_obj.salary_employee = employee
                form_obj.prepared_by = self.request.user
                form_obj.total_conveyance= conveyance
                form_obj.total_food_allowance = food_allowance
                form_obj.total_medical_allowance = medical_allowance
                form_obj.total_house_rent = house_rent
                form_obj.total_mobile_allowance = mobile_allowance
                form_obj.total_bonus =festival_bonus
                form_obj.total_salary = total_salary_value
                form_obj.save()
                messages.success(self.request, "Salary Added Successfully")
            
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
     
    
    
     
        
    
    


