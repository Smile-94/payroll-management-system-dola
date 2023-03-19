from django.urls import path

# Views
from reciption.views import reciption_main
from reciption.views import manage_attendance
from reciption.views import manage_sortleave
from reciption.views import manage_profile
from reciption.views import manage_leave
from reciption.views import manage_salary
from reciption.views import other_info

app_name = 'reception'

# Reception Main
urlpatterns = [
    path('reception/', reciption_main.ReceptionView.as_view(), name='reception_home'),
    
]

# manage attendance
urlpatterns += [
    path('add-attendance/', manage_attendance.AddAttendanceView.as_view(), name='add_attendance'),
    path('attendance-list/', manage_attendance.AttendanceListView.as_view(), name='attendance_list'),
    path('update-attendance/<int:pk>/', manage_attendance.UpdateAttendaceView.as_view(), name='update_attendance'),
    path('delete-attendance/<int:pk>/', manage_attendance.DeleteAttendanceView.as_view(), name='delete_attendance'),
]

# manage sortleave
urlpatterns += [
    path('sortleave-list/', manage_sortleave.SortleaveListView.as_view(), name='sortleave_list'),
    path('issued_sortleave/', manage_sortleave.AddSortleaveView.as_view(), name='issued_sortleave'),
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
    path('appliy-leave-receptionist/', manage_leave.ReceptionAddLeaveApplicationView.as_view(), name="apply_leave_receptionist" ),
    path('update-leave-receptionist/<int:pk>/', manage_leave.ReceptionLeaveApplicationUpdateView.as_view(), name="update_leave_receptionist" ),
    path('leave-details-receptionist/<int:pk>/', manage_leave.ReceptionLeaveApplicationDetailsView.as_view(), name="leave_details_receptionist" ),
]

# Manage Salary
urlpatterns += [
    path('receptionist-monthly-salary-list/', manage_salary.RecptionMonthlySalaryListView.as_view(), name='receptionist_monthly_salary_list'),
    path('receptionist-salary-details/<int:pk>/', manage_salary.ReceptionMonthlySalaryDetailsView.as_view(), name='receptionist_salary_details'),
]

# Other info
urlpatterns += [
    path('receptonist-permited-leave', other_info.ReceptionPermitedLeaveView.as_view(), name='receptonist_permited_leave'),
    path('receptonist-permited-latepresent', other_info.ReceptionPermitedLatePresentView.as_view(), name='receptonist_permited_latepresent'),
    path('receptonist-permited-sortleave', other_info.ReceptionPermitedSortleaveView.as_view(), name='receptonist_permited_sortleave'),
    path('receptonist-monthly-holiday', other_info.ReceptionMonthlyHolidayView.as_view(), name='receptonist_monthly_holiday'),
    path('receptonist-notice-list', other_info.ReceptionNoticeView.as_view(), name='receptonist_notice_list'),
    path('receptonist-notice-details<int:pk>/', other_info.ReceptionNoticeDetailsView.as_view(), name='receptonist_notice_details'),
]


