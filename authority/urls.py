from django.urls import path

# Views File
from authority.views import authority_main
from authority.views import manage_employee
from authority.views import admin_settings
from authority.views import salary_settings
from authority.views import manage_salary
from authority.views import manage_leave
from authority.views import manage_notic


app_name = 'authority'

urlpatterns = [
    path('authority/', authority_main.AdminView.as_view(), name='authority'),
]

# Manage Employee
urlpatterns += [
    path('add-employee/',  manage_employee.AddEmpolyeeView.as_view(), name='add_employee'),
    path('employee-list/', manage_employee.EmployeeListView.as_view(), name='employee_list'),
    path('employee-details/<int:pk>/', manage_employee.EmployeeDetailView.as_view(), name='employee_details'),
    path('edit_employee/<int:pk>/', manage_employee.EditEmployeeView.as_view(), name='edit_employee'),
    path('edit_address/<int:pk>/', manage_employee.EditEmployeeAddressView.as_view(), name='edit_address'),
    path('edit_salary/<int:pk>/', manage_employee.EditEmployeeSalaryView.as_view(), name='edit_salary'),
    
]

# manage salary:
urlpatterns += [
    path('salary-employee-list/', manage_salary.EmployeeSalaryListView.as_view(), name='salary_employee_list' ),
    path('calculated-salary-list/', manage_salary.MonthlyCalculatedSalaryListView.as_view(), name='calculated_salary_list' ),
    path('monthly-salary/<int:pk>/', manage_salary.MonthilySalaryCalculationView.as_view(), name='monthily_salary' ),
    path('employee-monthly-salary/<int:pk>/', manage_salary.EmployeeMonthlySalaryListView.as_view(), name='employee_monthily_salary' ),
    path('monthly-salary-details/<int:pk>/', manage_salary.MonthlySalaryDetailsView.as_view(), name='monthly_salary_details' ),
    path('update-calculated-salary/<int:pk>/', manage_salary.UpdateCalculatedSalaryView.as_view(), name='update_calculated_salary' ),
    path('delete-calculated-salary/<int:pk>/', manage_salary.DeleteCalculatedSalaryView.as_view(), name='delete_calculated_salary' ),
]

# Manage Leave
urlpatterns += [
    path('leave-application-list/', manage_leave.LeaveApplicationListView.as_view(), name='leave_application_list'),
    path('leave-application-details/<int:pk>/', manage_leave.LeaveApplicationDetailsView.as_view(), name='leave_application_details'), 
    path('accept-leave-application/<int:pk>/', manage_leave.LeaveApplicationAcceptView.as_view(), name='accept_leave_application'), 
    path('reject-leave-application/<int:pk>/', manage_leave.LeaveApplicationRejectView.as_view(), name='reject_leave_application'), 
    path('accepted-leave-application/', manage_leave.LeaveApplicationAcceptedListView.as_view(), name='accepted_leave_application'), 
    path('rejected-leave-application/', manage_leave.LeaveApplicationRjectedListView.as_view(), name='reject_leave_application'), 
    path('delete-leave-application/<int:pk>/', manage_leave.LeaveApplicationDeleteView.as_view(), name='delete_leave_application'), 
]



# add, update, delete admin settings
urlpatterns += [
    path('add-desgnation/', admin_settings.AddDesignationView.as_view(), name='add_designation'),
    path('update-designation/<int:pk>/', admin_settings.DesignationUpdateView.as_view(), name='update_designation'),
    path('delete-designation/<int:pk>/', admin_settings.DesignationDeleteView.as_view(), name='delete_designation'),
    path('add-office-time/', admin_settings.AddOfficeTimeView.as_view(), name='add_officetime'),
    path('update-office-time/<int:pk>/', admin_settings.UpdateOfficeTimeView.as_view(), name='update_officetime'),
    path('add-permited-leave/', admin_settings.AddPermitedLeaveView.as_view(), name='add_permited_leave'),
    path('update-permited-leave/<int:pk>/', admin_settings.UpdateMonthlyPermitedLeaveView.as_view(), name='update_permited_leave'),
    path('delete-permited-leave/<int:pk>/', admin_settings.DeleteMonthlyPermitedLeaveView.as_view(), name='delete_permited_leave'),
    path('add-late-present/', admin_settings.AddPermitedLatePresentView.as_view(), name='add_permited_latepresent'),
    path('update-late-present/<int:pk>/', admin_settings.UpdatePermitedLatePresentView.as_view(), name='update_permited_latepresent'),
    path('delete-late-present/<int:pk>/', admin_settings.DeletePermitedLatePresentView.as_view(), name='delete_permited_latepresent'),
    path('add-sort-leave/', admin_settings.AddPermitedSortLeaveView.as_view(), name='add_permited_sortleave'),
    path('update-sort-leave/<int:pk>/', admin_settings.UpdatePermitedSortLeaveView.as_view(), name='update_permited_sortleave'),
    path('delete-sort-leave/<int:pk>/', admin_settings.DeletePermitedSortLeaveView.as_view(), name='delete_permited_sortleave'),
    path('add-weekly-offday/', admin_settings.AddWeeklyOffDayView.as_view(), name='add_weekly_offday'),
    path('update-weekly-offday/<int:pk>/', admin_settings.UpdateWeeklyOffdayView.as_view(), name='update_weekly_offday'),
    path('delete-weekly-offday/<int:pk>/', admin_settings.DeleteWeeklyOffdayView.as_view(), name='delte_weekly_offday'),
    
]

# Manage Notice
urlpatterns += [
   path('add-notice', manage_notic.AddNoticeView.as_view(),name='add_notice'),
   path('update-notice/<int:pk>/', manage_notic.UpdateNoticeView.as_view(),name='update_notice'),
   path('notice-details/<int:pk>/', manage_notic.NoticeDetailsView.as_view(),name='notice_details'),
   path('delete-notice/<int:pk>/', manage_notic.DeleteNoticeView.as_view(),name='delete_notice'),
]



# Add, Update, Delete Payroll Months
urlpatterns += [
    path('add-payroll-month/', salary_settings.AddPayrollMonthView.as_view(), name='add_payrollmonth'),
    path('update-payroll-month/<int:pk>/', salary_settings.UpdatePayrollMonthView.as_view(), name='update_payrollmonth'), 
    path('add-offday/', salary_settings.AddMonthlyOffDayView.as_view(), name='add_offday'), 
    path('update-offday/<int:pk>/', salary_settings.UpdateMonthlyOffdayView.as_view(), name='update_offday'), 
    path('delete-offday/<int:pk>/', salary_settings.DeleteMonthlyOffdayView.as_view(), name='delete_offday'), 
    path('add-holiday/', salary_settings.AddMonthlyHoidayView.as_view(), name='add_holiday'), 
    path('update-holiday/<int:pk>/', salary_settings.UpdateMonthlyHolidayView.as_view(), name='update_holiday'), 
    path('delete-holiday/<int:pk>/', salary_settings.DeleteMonthlyHolidayView.as_view(), name='delete_holiday'), 
]

# Add , Update, delte Festival Bonus
urlpatterns += [
    path('festival-bonus/', salary_settings.FestivalBonusView.as_view(), name='festival_bonus'),
    path('festival-update/<int:pk>/', salary_settings.FestivalBonusUpdateView.as_view(), name='update_festival'),
]
