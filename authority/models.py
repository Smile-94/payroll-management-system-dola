from django.db import models

# Create your models here.

class OfficeTime(models.Model):
    office_start=models.TimeField(auto_now=False, auto_now_add=False)
    office_end=models.TimeField(auto_now=False, auto_now_add=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
