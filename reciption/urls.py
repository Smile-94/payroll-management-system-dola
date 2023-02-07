from django.urls import path

# Views
from reciption.views import ReceptionView
from reciption.views import AddAttendanceView
from reciption.views import AttendanceListView
from reciption.views import AddSortleaveView
from reciption.views import SortleaveListView
from reciption.views import SortLeaveUpdateView
from reciption.views import SortLeaveDetailView
from reciption.views import SortleaveDeleteView

app_name = 'reception'

urlpatterns = [
    path('reception/', ReceptionView.as_view(), name='reception_home'),
    path('add-attendance/', AddAttendanceView.as_view(), name='add_attendance'),
    path('attendance-list/', AttendanceListView.as_view(), name='attendance_list'),
    path('sortleave-list/', SortleaveListView.as_view(), name='sortleave_list'),
    path('add_sortleave/', AddSortleaveView.as_view(), name='add_sortleave'),
    path('sortleave-detail/<int:pk>/', SortLeaveDetailView.as_view(), name='sortleave_detail'),
    path('sortleave-update/<int:pk>/', SortLeaveUpdateView.as_view(), name='sortleave_update'),
    path('sortleave-delete/<int:pk>/', SortleaveDeleteView.as_view(), name='sortleave_delete'),
]
