from django.shortcuts import render

from django.views.generic import TemplateView

#Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class AdminView(LoginRequiredMixin,TemplateView):
    template_name='authority/admin.html'
