from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from django.contrib.auth.models import User
from .models import Profile
from .utils import email_task

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )

        email_task(subject='Welcome To DevSearch', message='We are glad you signed up!', receivers_list=[profile.email])

@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()

@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = instance.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()