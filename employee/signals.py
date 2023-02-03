from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from accounts.models import User
from employee.models import EmployeeInfo


@receiver(post_save, sender=User)
def create_employee_info(sender, instance, created, *args, **kwargs):
    if created and instance.is_employee:
        EmployeeInfo.objects.create(info_of=instance)


@receiver(post_save, sender=User)
def save_employee_info(sender, instance, *args, **kwargs):
    if instance.is_employee:
        instance.employee_info.save()