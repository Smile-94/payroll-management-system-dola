from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
# from django.contrib.auth.models import User
from accounts.models import User
from accounts.models import Profile
from accounts.models import PresentAddress
from accounts.models import PermanentAddress

# To automatically create profile for user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_present_address(sender, instance, created, *args, **kwargs):
    if created:
        PresentAddress.objects.create(address_of=instance)


@receiver(post_save, sender=User)
def save_present_address(sender, instance, *args, **kwargs):
    instance.present_address.save()


@receiver(post_save, sender=User)
def create_permanent_address(sender, instance, created, *args, **kwargs):
    if created:
        PermanentAddress.objects.create(address_of=instance)


@receiver(post_save, sender=User)
def save_permanent_address(sender, instance, *args, **kwargs):
    instance.permanent_address.save()