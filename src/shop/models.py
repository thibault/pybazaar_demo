from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Product(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(
        _('Name'),
        max_length=255)
    initial_price = models.PositiveIntegerField(
        _('Initial price'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return self.name
