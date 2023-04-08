# for generating pdf
from django.views.generic.detail import DetailView
from django_xhtml2pdf.views import PdfMixin
from django.conf import settings

# Models
from accounts.models import User
from reciption.models import SortLeave
from authority.models import LeaveApplication
from employee.models import MonthlySalary


class EmployeePdfView(PdfMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = "report/profile_pdf.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['static_url'] = self.request.build_absolute_uri(settings.STATIC_URL)
        return context
    
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        filename = "profile_{0}.pdf".format(self.object.pk)
        response['Content-Disposition'] = 'filename="{}"'.format(filename)
        return response

class SortLeavePdfView(PdfMixin, DetailView):
    model = SortLeave
    context_object_name = 'sortleave'
    template_name = "report/sortleave_pdf.html"

 
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        filename = "sortleave_{0}.pdf".format(self.object.pk)
        response['Content-Disposition'] = 'filename="{}"'.format(filename)
        return response

class LeaveApplicationPdfView(PdfMixin, DetailView):
    model = LeaveApplication
    context_object_name = 'leave'
    template_name = 'report/leave_applicationpdf.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        filename = "leave_Application_{0}.pdf".format(self.object.pk)
        response['Content-Disposition'] = 'filename="{}"'.format(filename)
        return response

class SalaryDetailsPdfview(PdfMixin, DetailView):
    model = MonthlySalary
    context_object_name = 'salary'
    template_name = 'report/monthly_sslarypdf.html'

    def get_context_data(self, **kwargs):
        query_obj = self.get_object()
        total_salary = query_obj.total_salary
        total_diduct = query_obj.total_diduct
        context = super().get_context_data(**kwargs)
        context["total_salary_pay"] =round(total_salary-total_diduct)
        return context
    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        filename = "Salary_Application_{0}.pdf".format(self.object.pk)
        response['Content-Disposition'] = 'filename="{}"'.format(filename)
        return response


