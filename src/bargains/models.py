from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from shop.models import Product


class Bargain(models.Model):
    buyer = models.ForeignKey(User)
    product = models.ForeignKey(Product)

    def get_absolute_url(self):
        return reverse('bargain', args=[self.id])
