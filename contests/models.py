from django.db import models
from django.utils.translation import gettext_lazy as _ 

from accounts.models import CustomUser

from .utils import generate_code

from datetime import datetime

# Create your models here.
class Contest(models.Model):
    name = models.CharField(_("name"), max_length=150, blank=False)
    description = models.TextField()
    organizer = models.ForeignKey(CustomUser, models.CASCADE)
    max_contestants = models.PositiveIntegerField()
    date = models.DateTimeField(default=datetime.now())
    contest_code = models.CharField(
        _("contest code"), max_length=12, default=generate_code
    )

    def __str__(self):
        return str(self.name)


class Contestant(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE)
    contest = models.ForeignKey(Contest, models.CASCADE)
    name = models.CharField(_("name"), max_length=150, blank=False)
    manifesto = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user.name) + ' ' + str(self.contest.name)


