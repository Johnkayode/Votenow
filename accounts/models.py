from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _ 

from .utils import generate_code


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("email address cannot be left empty!"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True) 
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser must set is_staff to True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must set is_superuser to True"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), blank=False, unique=True)
    name = models.CharField(_("name"), max_length=150, blank=False)
    is_confirmed = models.BooleanField(_("is confirmed"), default=False)
    is_organizer = models.BooleanField(_("is organizer"), default=False)
    is_contester = models.BooleanField(_("is contestant"), default=False)
    confirmation_code = models.IntegerField(
        _("confirmation code"), default=generate_code
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Contestant(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE)
    name = models.CharField(_("name"), max_length=150, blank=False)
    about = models.CharField(_("name"), max_length=150, blank=True)
    def __str__(self):
        return self.user.name

class Organizer(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE)
    name = models.CharField(_("name"), max_length=150, blank=False)
    about = models.CharField(_("name"), max_length=150, blank=True)
    def __str__(self):
        return self.user.name