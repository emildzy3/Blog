

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .models import ProfileAuthor


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_author:
            ProfileAuthor.objects.create(author=instance)
    if not ProfileAuthor:
        instance.profileauthor.save()
