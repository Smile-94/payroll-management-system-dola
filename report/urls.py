from django.urls import path

from report.views import pdf_report


app_name = 'report'

urlpatterns = [
    path('profile-pdf/<int:pk>/', pdf_report.EmployeePdfView.as_view(), name="profile_pdf"),
    path('sortleave-pdf/<int:pk>/', pdf_report.SortLeavePdfView.as_view(), name="sortleave_pdf"),
    path('leaveapplication-pdf/<int:pk>/', pdf_report.LeaveApplicationPdfView.as_view(), name="leaveapplication_pdf"),
    path('salary-details-pdf/<int:pk>/', pdf_report.SalaryDetailsPdfview.as_view(), name="salary_details_pdf"),
]
