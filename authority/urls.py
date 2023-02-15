from django.urls import path

# views
from authority.views import AdminView
from authority.views import AddDesignationView
from authority.views import DesignationListView
from authority.views import DesignationUpdateView
from authority.views import DesignationDeleteView
from authority.views import AddEmpolyeeView
from authority.views import EmployeeListView
from authority.views import EditEmployeeView
from authority.views import EditEmployeeAddressView
from authority.views import EditEmployeeSalaryView
from authority.views import EmployeeDetailView
from authority.views import AddOfficeTimeView
from authority.views import UpdateOfficeTimeView

# Payroll Months
from authority.views import AddPayrollMonthView
from authority.views import UpdatePayrollMonthView

# Festival Bonus
from authority.views import FestivalBonusView
from authority.views import FestivalBonusUpdateView

app_name = 'authority'

urlpatterns = [
    path('authority/', AdminView.as_view(), name='authority'),
    path('add-employee/', AddEmpolyeeView.as_view(), name='add_employee'),
    path('employee-list/', EmployeeListView.as_view(), name='employee_list'),
    path('employee-details/<int:pk>/', EmployeeDetailView.as_view(), name='employee_details'),
    path('edit_employee/<int:pk>/', EditEmployeeView.as_view(), name='edit_employee'),
    path('edit_address/<int:pk>/', EditEmployeeAddressView.as_view(), name='edit_address'),
    path('edit_salary/<int:pk>/', EditEmployeeSalaryView.as_view(), name='edit_salary'),
    path('add-desgnation/', AddDesignationView.as_view(), name='add_designation'),
    path('designation-list/', DesignationListView.as_view(), name='designation_list'),
    path('update-designation/<int:pk>/', DesignationUpdateView.as_view(), name='update_designation'),
    path('delete-designation/<int:pk>/', DesignationDeleteView.as_view(), name='delete_designation'),
    path('add-office-time/', AddOfficeTimeView.as_view(), name='add_officetime'),
    path('update-office-time/<int:pk>/', UpdateOfficeTimeView.as_view(), name='update_officetime')
]

# Add, Update, Delete Payroll Months
urlpatterns += [
    path('add-payroll-month/', AddPayrollMonthView.as_view(), name='add_payrollmonth'),
    path('update-payroll-month/<int:pk>/', UpdatePayrollMonthView.as_view(), name='update_payrollmonth'), 
]

# Add , Update, delte Festival Bonus
urlpatterns += [
    path('festival-bonus/', FestivalBonusView.as_view(), name='festival_bonus'),
    path('festival-update/<int:pk>/', FestivalBonusUpdateView.as_view(), name='update_festival'),
]
