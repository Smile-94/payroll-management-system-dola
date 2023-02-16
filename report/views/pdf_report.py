# for generating pdf
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django_xhtml2pdf.views import PdfMixin
from django.conf import settings

# Models
from accounts.models import User


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