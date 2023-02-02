from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse


# classbased view classes
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin


#Models
from accounts.models import User
from accounts.models import Profile
from employee.models import DesignationInfo


# forms 
from employee.forms import DesignationInfoForm
from accounts.forms import EmployeeSignUpForm
from accounts.forms import ProfileForm


# Create your views here.
class AddEmpolyeeView(CreateView):
    model=User
    form_class=EmployeeSignUpForm
    success_url=reverse_lazy('authority:authority')
    template_name='authority/add_employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] ="Create Employee Accounts" 
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            user=form.save(commit=False)
            user.is_employee=True
            user.save()
            messages.success(self.request, "Employee Accounts Created Success Fully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "email or password invalid trya aging")
        return super().form_invalid(form)
    

class EmployeeListView(ListView):
    model=User
    context_object_name='employees'
    template_name='authority/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] ="Employee List" 
        return context
    

class AdminView(LoginRequiredMixin,TemplateView):
    template_name='authority/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Admin Panel" 
        return context
    

class AddDesignationView(CreateView):
    model=DesignationInfo
    form_class=DesignationInfoForm
    template_name='authority/add_designation.html'
    success_url=reverse_lazy('authority:add_designation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] ='Add Designation'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Designation Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went worg please try agaign")
        return super().form_invalid(form)


class DesignationListView(ListView):
    model=DesignationInfo
    fields=('designation','department','created_at','updated_at')
    context_object_name='designations'
    template_name='authority/designation_list.html'

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
        
class DesignationUpdateView(UpdateView):
    model=DesignationInfo
    fields=('designation','department','description')
    template_name='authority/add_designation.html'
    success_url=reverse_lazy('authority:designation_list')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Designation" 
        return context

    def form_valid(self, form):
        messages.success(self.request, "Designation Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "some thing went wrong try againg")
        return super().form_invalid(form)

class DesignationDeleteView(DeleteView):
    model=DesignationInfo
    template_name='authority/delete_designation.html'
    context_object_name='designation'
    success_url=reverse_lazy('authority:designation_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active=False
        self.object.save()
        return redirect(success_url)

