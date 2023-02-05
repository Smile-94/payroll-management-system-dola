import django_filters
from django import forms

from accounts.models import User


class EmployeeListFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = {
            'email': {'exact'},
        }
        