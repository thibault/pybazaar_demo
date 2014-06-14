import pickle

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from pybazaar_protocol.negotiation import Negotiation
from pybazaar_protocol.messages import BargainInitDetails

from shop.models import Product


class Bargain(models.Model):
    buyer = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    nego_buyer = models.TextField()
    nego_seller = models.TextField()

    def get_absolute_url(self):
        return reverse('bargain', args=[self.id])

    def save(self):
        if not self.id:
            self.init_negotiation()

        return super(Bargain, self).save()

    def init_negotiation(self):
        nego_buyer = Negotiation(role=Negotiation.ROLE_BUYER)
        nego_seller = Negotiation(role=Negotiation.ROLE_SELLER)

        details = BargainInitDetails('', '')
        init_msg = nego_buyer.build_bargain_init(details)

        nego_seller.check_bargain_init(init_msg)
        self.nego_buyer = pickle.dumps(nego_buyer)
        self.nego_seller = pickle.dumps(nego_seller)
