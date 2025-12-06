import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from user.manager import UserManager
from utils.user_utils import UserRole, Gender


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        abstract = True


class User(AbstractUser, Timestamp):
    username = None
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=14, unique=True)
    role = models.IntegerField(
        choices=UserRole.get_choices(), default=UserRole.EMPLOYEE.value
    )

    def __str__(self):
        return self.name

    @property
    def role_name(self):
        if self.role == 1:
            return "Admin"
        return "Employee"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    objects = UserManager()


class Profile(Timestamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.IntegerField(
        choices=Gender.get_gender(), blank=True, null=True, default=None
    )
    avatar = models.ImageField(upload_to="avatar/%m/%d", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, default="")
    street = models.CharField(max_length=255, blank=True, default="")
    state = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=255, blank=True, default="")
    zip_code = models.CharField(max_length=255, blank=True, default="")
    latitude = models.CharField(max_length=100, blank=True, default="")
    longitude = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return self.user.fullname

    @property
    def get_gender(self):
        return


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)
        return profile


post_save.connect(create_user_profile, sender=User)
