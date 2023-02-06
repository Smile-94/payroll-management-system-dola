from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


# Filters Class
from authority.filters import EmployeeListFilter


# class-based view classes
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin


# Models
from accounts.models import User
from accounts.models import Profile
from accounts.models import PresentAddress
from accounts.models import PermanentAddress
from employee.models import EmployeeInfo
from employee.models import DesignationInfo
from authority.models import OfficeTime


# forms 
from employee.forms import DesignationInfoForm
from accounts.forms import EmployeeSignUpForm
from accounts.forms import ProfileForm
from accounts.forms import PresentAddressForm
from accounts.forms import PermanentAddressForm
from employee.forms import EmployeeInfoForm
from employee.forms import EmployeeSalaryForm
from authority.forms import OfficeTimeForm


# Create your views here.
class AdminView(LoginRequiredMixin, TemplateView):
    template_name = 'authority/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Admin Panel" 
        return context
    

class AddEmpolyeeView(LoginRequiredMixin, CreateView):
    model = User
    form_class = EmployeeSignUpForm
    success_url = reverse_lazy('authority:authority')
    template_name = 'authority/add_employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Employee Accounts"
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_employee = True
            user.save()
            messages.success(self.request, "Employee Accounts Created Success Fully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "email or password invalid try aging")
        return super().form_invalid(form)
   

class EmployeeListView(LoginRequiredMixin, ListView):
    queryset = User.objects.all()
    filterset_class = EmployeeListFilter
    template_name = 'authority/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee List"
        context["employees"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    queryset = User.objects.all()
    template_name = 'authority/employee_detail.html'

    def get_context_data(self, **kwargs):
        user_obj = User.objects.get(id=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Details"
        context["profile"] = Profile.objects.get(user=user_obj)
        context["employee_info"] = EmployeeInfo.objects.get(info_of=user_obj)
        context["present_address"] = PresentAddress.objects.get(address_of=user_obj)
        context["permanent_address"] = PermanentAddress.objects.get(address_of=user_obj)
        return context
    

class EditEmployeeView(LoginRequiredMixin, UpdateView):
    model = Profile
    model2 = EmployeeInfo
    form_class = ProfileForm
    form_class2 = EmployeeInfoForm
    template_name = 'authority/add_employee_info.html'
    success_url = reverse_lazy('authority:employee_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Employee Info"
        user_object = User.objects.get(id=self.kwargs.get('pk'))
        context["title"] = "Add Employee info"
        context["form"] = self.form_class(instance=user_object.profile)
        context["form2"] = self.form_class2(instance=user_object.employee_info)
        return context
         
    def post(self, request, *args, **kwargs):
        user_object = User.objects.get(id=self.kwargs.get('pk'))
        form = self.form_class(request.POST, request.FILES, instance=user_object.profile)
        form2 = self.form_class2(request.POST, request.FILES, instance=user_object.employee_info)
        return self.form_valid(form, form2)
    
    def form_valid(self, form, form2):
        try:
            if form.is_valid() and form2.is_valid():
                user = form.save(commit=False)
                info = form2.save(commit=False)
                user.profile = User.objects.get(id=self.kwargs.get('pk'))
                info.info_of = User.objects.get(id=self.kwargs.get('pk'))
                user.save()
                info.save()
                messages.success(self.request, "Employee Info Updated Successfully")
            return super().form_valid(form)

        except Exception as e:
            print(e)
            return super().form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Some thing wrong try again")
        return super().form_invalid(form)


class EditEmployeeAddressView(LoginRequiredMixin, UpdateView):
    model = PresentAddress
    model2 = PermanentAddress
    form_class = PresentAddressForm
    form_class2 = PermanentAddressForm
    template_name = 'authority/edit_address.html'
    success_url = reverse_lazy('authority:employee_list')

    def get_context_data(self, **kwargs):
        user_obj = User.objects.get(id=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context["title"] = "Add/Edit Address"
        context["present_address"] = self.form_class(instance=user_obj.present_address)
        context["permanent_address"] = self.form_class2(instance=user_obj.permanent_address)
        return context
    
    def post(self, request, *args, **kwargs):
        user_obj = User.objects.get(id=self.kwargs.get('pk'))
        form1 = self.form_class(request.POST, instance=user_obj.present_address)
        form2 = self.form_class2(request.POST, instance=user_obj.permanent_address)
        return self.form_valid(form1, form2)
    
    def form_valid(self, form, form2):
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(self.request, "Address Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong try again")
        return super().form_invalid(form)


class EditEmployeeSalaryView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EmployeeSalaryForm
    template_name = 'authority/edit_salary.html'
    success_url = reverse_lazy('authority:employee_list')

    def get_context_data(self, **kwargs):
        user_obj = User.objects.get(id=self.kwargs.get('pk'))
        employee_info_obj = EmployeeInfo.objects.get(info_of=user_obj)
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Salary"
        context["form"] = self.form_class(instance=employee_info_obj.salary_info)
        return context
    
    def post(self, request, *args, **kwargs):
        user_obj = User.objects.get(id=self.kwargs.get('pk'))
        employee_info_obj = EmployeeInfo.objects.get(info_of=user_obj)
        form = self.form_class(request.POST, instance=employee_info_obj.salary_info)
        return self.form_valid(form)
    
    def form_valid(self, form):
        if form.is_valid:
            form.save()
            messages.success(self.request, "Employee Salary Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something goes wrong try again")
        return super().form_invalid(form)
    

class AddDesignationView(LoginRequiredMixin, CreateView):
    model = DesignationInfo
    form_class = DesignationInfoForm
    template_name = 'authority/add_designation.html'
    success_url = reverse_lazy('authority:add_designation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Designation'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Designation Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong please try again")
        return super().form_invalid(form)


class DesignationListView(LoginRequiredMixin, ListView):
    model = DesignationInfo
    fields = ('designation', 'department', 'created_at', 'updated_at')
    context_object_name = 'designations'
    template_name = 'authority/designation_list.html'

    def get_queryset(self):
        try:
            return DesignationInfo.objects.filter(is_active=True)
        except Exception as e:
            print(e)
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Designation List" 
        return context


class DesignationUpdateView(LoginRequiredMixin, UpdateView):
    model = DesignationInfo
    fields = ('designation', 'department', 'description')
    template_name = 'authority/add_designation.html'
    success_url = reverse_lazy('authority:designation_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Designation" 
        return context

    def form_valid(self, form):
        messages.success(self.request, "Designation Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "some thing went wrong try again")
        return super().form_invalid(form)


class DesignationDeleteView(LoginRequiredMixin, DeleteView):
    model = DesignationInfo
    template_name = 'authority/delete_designation.html'
    context_object_name = 'designation'
    success_url = reverse_lazy('authority:designation_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return redirect(success_url)

class AddOfficeTimeView(CreateView):
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


class UpdateOfficeTimeView(UpdateView):
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
