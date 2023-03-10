
#Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from reciption.permissions import ReceptionPassesTestMixin

# Django Generic classes
from django.views.generic import ListView
from django.views.generic import DetailView

# Models
from authority.models import MonthlyPermitedLeave
from authority.models import PermitedLatePresent
from authority.models import PermitedSortLeave
from authority.models import MonthlyHoliday
from authority.models import Notice

# Filters
from authority.filters import MonthlyHolidayFilter
from authority.filters import NoticeFilter


class ReceptionPermitedLeaveView(LoginRequiredMixin, ReceptionPassesTestMixin, ListView):
    model = MonthlyPermitedLeave
    template_name = 'reception/permited_leave_reception.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Monthly Permited Leave' 
        context["months"] = MonthlyPermitedLeave.objects.filter(is_active=True) 
        return context

class ReceptionPermitedLatePresentView(LoginRequiredMixin, ReceptionPassesTestMixin, ListView):
    model = PermitedLatePresent
    queryset = PermitedLatePresent.objects.filter(is_active=True).order_by('-id')
    template_name = 'reception/reception_permited_late_present.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Late Present'
        context["presents"] = self.queryset
        return context

class ReceptionPermitedSortleaveView(LoginRequiredMixin, ReceptionPassesTestMixin, ListView):
    model = PermitedSortLeave
    queryset = PermitedSortLeave.objects.filter(is_active=True).order_by('-id')
    template_name = 'reception/reception_permited_sort_leave.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Permited Sort Leave'
        context["sortleaves"] = self.queryset
        return context

class ReceptionMonthlyHolidayView(LoginRequiredMixin, ReceptionPassesTestMixin, ListView):
    model = MonthlyHoliday
    queryset = MonthlyHoliday.objects.filter(is_active= True)
    filterset_class = MonthlyHolidayFilter
    template_name = 'reception/reception_monthly_holyday.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Holiday"
        context["holidays"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context


class ReceptionNoticeView(LoginRequiredMixin, ReceptionPassesTestMixin, ListView):
    model = Notice
    queryset = Notice.objects.filter(is_active= True)
    filterset_class = NoticeFilter
    form_class = NoticeFilter
    template_name = 'reception/reception_notice_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Off Day"
        context["notices"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

class ReceptionNoticeDetailsView(LoginRequiredMixin, ReceptionPassesTestMixin, DetailView):
    model = Notice
    context_object_name = 'notice'
    template_name = 'reception/reception_notice_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notice Details"
        return context