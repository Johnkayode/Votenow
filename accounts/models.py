import qrcode
from io import StringIO, BytesIO
import base64


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _ 

from .utils import generate_code, encode_data


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
    qr_code = models.ImageField(upload_to='qrcodes', blank=True, null=True)
    confirmation_code = models.IntegerField(
        _("confirmation code"), default=generate_code
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
 
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_qrcode(self):
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=6, border=0)
        email = self.email
        data = encode_data(email)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)
        filename = f'{self.name}'
        filebuffer = InMemoryUploadedFile(buffer,None, filename, 'image/png',buffer.getbuffer().nbytes, None)
        self.qr_code.save(filename, filebuffer)

