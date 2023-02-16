from django.urls import path

from report.views import pdf_report


app_name = 'report'

urlpatterns = [
    path('profile-pdf/<int:pk>/', pdf_report.EmployeePdfView.as_view(), name="profile_pdf"),
]
