from django.contrib import admin

# models
from authority.models import OfficeTime
from authority.models import PayrollMonth
from authority.models import FestivalBonus


# Register your models here.
@admin.register(PayrollMonth)
class PayrollMonthAdmin(admin.ModelAdmin):
    list_display = ('month','year','from_date','to_date')
    list_filter = ('month',)
    list_per_page= 50

@admin.register(FestivalBonus)
class FestivalBonusAdmin(admin.ModelAdmin):
    list_display=('festival_name','bonus_percentage','created_at','modified_at')

@admin.register(OfficeTime)
class SetOfficeTimeAdmin(admin.ModelAdmin):
    list_display = ('office_start', 'office_end', 'modified_at', 'created_at')

