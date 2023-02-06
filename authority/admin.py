from django.contrib import admin

# models
from authority.models import OfficeTime


# Register your models here.
@admin.register(OfficeTime)
class SetOfficeTimeAdmin(admin.ModelAdmin):
    list_display = ('office_start', 'office_end', 'modified_at', 'created_at')
