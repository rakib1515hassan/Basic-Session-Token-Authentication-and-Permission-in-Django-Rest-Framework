from django.db import models
from django.contrib.auth.models import User

## NOTE For Create Toke, When User Create. That's why we use Django signal.------------
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
# -------------------------------------------------------------------------------------

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    gender = models.CharField(max_length=15, choices = (
        ('Male', 'Male'),
        ('Felame', 'Female'),
        ('Others', 'Others'),
    ))

    def __str__(self):
        return self.user.username

