from django.urls import path

# import views
from employee.views import employee_main
from employee.views import manage_leave

app_name='employee'

urlpatterns = [
    path('employee/', employee_main.EmployeeHomeView.as_view(), name='employee')
    
]

# Manage Leave
urlpatterns += [
    path('appliy-leave/', manage_leave.AddLeaveApplicationView.as_view(), name="apply_leave" ),
    path('update-leave/<int:pk>/', manage_leave.LeaveApplicationUpdateView.as_view(), name="update_leave" ),
]

