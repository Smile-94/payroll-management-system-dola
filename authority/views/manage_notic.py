from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

# Generic Views
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.views.generic import DeleteView

# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permission import AdminPassesTestMixin

# Models
from authority.models import Notice

# Forms
from authority.forms import NoticeForm

# Filter Class
from authority.filters import NoticeFilter


class AddNoticeView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Notice
    queryset = Notice.objects.filter(is_active= True)
    filterset_class = NoticeFilter
    form_class = NoticeForm
    template_name = 'authority/add_notice.html'
    success_url = reverse_lazy('authority:add_notice')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Off Day"
        context["notices"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        form_obj.created_by = self.request.user
        messages.success(self.request, "Notice added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Something Went Worng please try again")
        return super().form_invalid(form)


class UpdateNoticeView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'authority/add_notice.html'
    success_url = reverse_lazy('authority:add_notice')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Notice"
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Notice Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Notice updated, try again!")
        return super().form_invalid(form)

class NoticeDetailsView(LoginRequiredMixin, AdminPassesTestMixin, DetailView):
    model = Notice
    context_object_name = 'notice'
    template_name = 'authority/notice_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notice Details"
        return context

class DeleteNoticeView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= Notice
    template_name = "authority/delete_notice.html"
    success_url = reverse_lazy('authority:add_notice')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Notice" 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)