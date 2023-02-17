from django.urls import path

# import views
from employee.views import employee_main

app_name='employee'

urlpatterns = [
    path('employee/', employee_main.EmployeeHomeView.as_view(), name='employee')
    
]
