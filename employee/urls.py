from django.urls import path

# import views
from employee.views import employee_main
from employee.views import manage_leave
from employee.views import manage_salary

app_name='employee'

urlpatterns = [
    path('employee/', employee_main.EmployeeHomeView.as_view(), name='employee'),
    
]

# Manage Leave
urlpatterns += [
    path('appliy-leave/', manage_leave.AddLeaveApplicationView.as_view(), name="apply_leave" ),
    path('update-leave/<int:pk>/', manage_leave.LeaveApplicationUpdateView.as_view(), name="update_leave" ),
    path('leave-details/<int:pk>/', manage_leave.LeaveApplicationDetailsView.as_view(), name="leave_details" ),
]

# Manage Salary
urlpatterns += [
    path('monthly-salary-list/', manage_salary.MonthlySalaryListView.as_view(), name='monthly_salary_list'),
    path('employee-salary-details/<int:pk>/', manage_salary.EmployeeMonthlySalaryDetailsView.as_view(), name='employee_salary_details'),
]


