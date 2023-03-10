from django.urls import path

# import views
from employee.views import employee_main
from employee.views import manage_leave
from employee.views import manage_salary
from employee.views import manage_profile
from employee.views import others_info

app_name='employee'

urlpatterns = [
    path('employee/', employee_main.EmployeeHomeView.as_view(), name='employee'),
    
]

# Manage Profile
urlpatterns += [
    path('profile-details-employee/<int:pk>/', manage_profile.EmployeeProfileDetailsView.as_view(), name='profile_details_emplyee') 
]

# Manage Leave
urlpatterns += [
    path('appliy-leave/', manage_leave.AddLeaveApplicationView.as_view(), name="apply_leave" ),
    path('update-leave/<int:pk>/', manage_leave.LeaveApplicationUpdateView.as_view(), name="update_leave" ),
    path('leave-details/<int:pk>/', manage_leave.LeaveApplicationDetailsView.as_view(), name="leave_details" ),
    path('employee_sort_leave/', manage_leave.EmployeeSortleaveListView.as_view(), name="employee_sort_leave" ),
    path('employee_sort_leave_details/<int:pk>/', manage_leave.EmployeeSortLeaveDetailView.as_view(), name="employee_sort_leave_details" ),
]

# Manage Salary
urlpatterns += [
    path('monthly-salary-list/', manage_salary.MonthlySalaryListView.as_view(), name='monthly_salary_list'),
    path('employee-salary-details/<int:pk>/', manage_salary.EmployeeMonthlySalaryDetailsView.as_view(), name='employee_salary_details'),
]

# Other info
urlpatterns += [
    path('employee-permited-leave/', others_info.EmployeePermitedLeaveView.as_view(), name='employee_permited_leave'),
    path('employee-permited-latepresent/', others_info.EmployeePermitedLatePresentView.as_view(), name='employee_permited_latepresent'),
    path('employee-permited-sortleave/', others_info.EmployeePermitedSortleaveView.as_view(), name='employee_permited_sortleave'),
    path('employee-monthly-holiday/', others_info.EmployeeMonthlyHolidayView.as_view(), name='employee_monthly_holiday'),
    path('employee-notice-list/', others_info.EmployeeNoticeView.as_view(), name='employee_notice'),
    path('employee-notice-details/<int:pk>/', others_info.EmployeeNoticeDetailsView.as_view(), name='employee_notice_details'),
]



