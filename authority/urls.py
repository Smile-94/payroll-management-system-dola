from django.urls import path

# views
from authority.views import AdminView
from authority.views import AddDesignationView
from authority.views import DesignationListView
from authority.views import DesignationUpdateView
from authority.views import DesignationDeleteView
from authority.views import AddEmpolyeeView
from authority.views import EmployeeListView

app_name='authority'

urlpatterns = [
    path('authority/', AdminView.as_view(), name='authority'),
    path('add-employee/',AddEmpolyeeView.as_view(),name='add_employee'),
    path('employee-list/',EmployeeListView.as_view(),name='employee_list'),
    path('add-desgnation/', AddDesignationView.as_view(), name='add_designation'),
    path('designation-list/', DesignationListView.as_view(), name='designation_list'),
    path('update-designation/<int:pk>/', DesignationUpdateView.as_view(), name='update_designation'),
    path('delete-designation/<int:pk>/', DesignationDeleteView.as_view(), name='delete_designation'),


]
