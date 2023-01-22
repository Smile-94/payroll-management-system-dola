from django.contrib import admin

# models
from accounts.models import User
from accounts.models import Profile
from accounts.models import PresentAddress
from accounts.models import PermanentAddress

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('email','is_employee','is_staff','is_active')
    search_fields=('email',)
    list_filter=('email','is_employee')
    list_per_page=50

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','first_name','last_name','gender','date_of_join')
    search_fields=('user','first_name','date_of_join')
    list_filter=('gender','date_of_join')
    aw_id_fields=('user',)
    list_per_page=50

@admin.register(PresentAddress)
class PresentAddressAdmin(admin.ModelAdmin):
    list_display=('address_of','present_village','present_post','present_upzila','present_district','present_post_code')
    search_fields=('address_of',)
    list_filter=('present_post_code','present_district','present_division')
    list_per_page=50

@admin.register(PermanentAddress)
class PermanentAddressAdmin(admin.ModelAdmin):
    list_display=('address_of','permanent_village','permanent_post','permanent_upzila','permanent_district','permanent_post_code')
    search_fields=('address_of',)
    list_filter=('present_division',)
    list_per_page=50



