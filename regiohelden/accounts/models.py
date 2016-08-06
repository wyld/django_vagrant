from django.db import models
from django.utils.translation import ugettext_lazy as _

from localflavor.generic.models import IBANField


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    iban = IBANField()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)
