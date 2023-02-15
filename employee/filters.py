import django_filters
from django import forms

# models
from employee.models import DesignationInfo


class DesignationInfoFilter(django_filters.FilterSet):
    
    designation = django_filters.CharFilter(lookup_expr='contains')
    

    class Meta:
        model = DesignationInfo
        fields = ('designation','department')

