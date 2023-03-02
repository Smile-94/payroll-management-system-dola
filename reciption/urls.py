from django.urls import path

# Views
from reciption.views import reciption_main
from reciption.views import manage_attendance
from reciption.views import manage_sortleave
from reciption.views import manage_profile
from reciption.views import manage_leave

app_name = 'reception'

# Reception Main
urlpatterns = [
    path('reception/', reciption_main.ReceptionView.as_view(), name='reception_home'),
    
]

# manage attendance
urlpatterns += [
    path('add-attendance/', manage_attendance.AddAttendanceView.as_view(), name='add_attendance'),
    path('attendance-list/', manage_attendance.AttendanceListView.as_view(), name='attendance_list'),
]

# manage sortleave
urlpatterns += [
    path('sortleave-list/', manage_sortleave.SortleaveListView.as_view(), name='sortleave_list'),
    path('add_sortleave/', manage_sortleave.AddSortleaveView.as_view(), name='add_sortleave'),
    path('sortleave-detail/<int:pk>/',manage_sortleave.SortLeaveDetailView.as_view(), name='sortleave_detail'),
    path('sortleave-update/<int:pk>/', manage_sortleave.SortLeaveUpdateView.as_view(), name='sortleave_update'),
    path('sortleave-delete/<int:pk>/', manage_sortleave.SortleaveDeleteView.as_view(), name='sortleave_delete'), 
]

# Manage Profile
urlpatterns += [
    path('profile-details/<int:pk>/', manage_profile.ProfileDetailsView.as_view(), name='profile_details') 
]

# Manage Leave
urlpatterns += [
    path('appliy-leave/', manage_leave.AddLeaveApplicationView.as_view(), name="apply_leave" ),
    path('update-leave/<int:pk>/', manage_leave.LeaveApplicationUpdateView.as_view(), name="update_leave" ),
    path('leave-details/<int:pk>/', manage_leave.LeaveApplicationDetailsView.as_view(), name="leave_details" ),
]


