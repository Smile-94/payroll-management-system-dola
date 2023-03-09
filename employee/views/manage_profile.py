# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# Generic View Class
from django.views.generic import DetailView

# MOdels
from accounts.models import User
from accounts.models import Profile
from accounts.models import PresentAddress
from accounts.models import PermanentAddress
from employee.models import EmployeeInfo


class EmployeeProfileDetailsView(LoginRequiredMixin, EmployeePassesTestMixin, DetailView):
    queryset = User.objects.all()
    context_object_name='user'
    template_name = 'employee/profile_details_employee.html'

    def get_context_data(self, **kwargs):
        user_obj = User.objects.get(id=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Details"
        context["profile"] = Profile.objects.get(user=user_obj)
        context["employee_info"] = EmployeeInfo.objects.get(info_of=user_obj)
        context["present_address"] = PresentAddress.objects.get(address_of=user_obj)
        context["permanent_address"] = PermanentAddress.objects.get(address_of=user_obj)
        return context