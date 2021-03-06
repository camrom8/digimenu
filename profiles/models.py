from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from index.helpers.validators import validate_phone


class Profile(models.Model):
    MALE = 'MA'
    FEMALE = 'FE'
    OTHER = 'OT'
    GENDER = [
        (MALE, _('Male')),
        (FEMALE, _('Femele')),
        (OTHER, _('other')),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField(blank=True, null=True, validators=[validate_phone])
    nickname = models.CharField(_('nickname'), max_length=20, default="none")
    gender = models.CharField(_('gender'), max_length=2, choices=GENDER, default=OTHER)
    address = models.CharField(_('address'), max_length=100, blank=True)
    photo = models.ImageField(upload_to="media/profiles", default="images/default/no_photo.png", null=True)
    company = models.CharField(_('company'), max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def get_absolute_url(self):
    #     return reverse('account:login')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance).save()


@receiver(post_save, sender=User())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
