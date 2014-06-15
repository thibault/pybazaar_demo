import pickle
import time

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from pybazaar_protocol.negotiation import Negotiation
from pybazaar_protocol.messages import BargainInitDetails, BargainRequestDetails
from bitcoin import address_to_script

from shop.models import Product
from wallet.models import Wallet


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

    def get_seller_address(self):
        wallet = Wallet.objects.get_for_user(self.product.owner)
        return wallet.pubkey

    def messages(self):
        nego = pickle.loads(self.nego_buyer)
        sent = iter(nego._msg_sent)
        received = iter(nego._msg_received)

        # Get rid of the initial BargainInit
        sent.next()

        has_sent = True
        has_received = True
        while has_sent or has_received:
            try:
                yield sent.next()
            except StopIteration:
                has_sent = False

            try:
                yield received.next()
            except StopIteration:
                has_received = False

    def init_negotiation(self):
        nego_buyer = Negotiation(role=Negotiation.ROLE_BUYER)
        nego_seller = Negotiation(role=Negotiation.ROLE_SELLER)

        details = BargainInitDetails('', '')
        init_msg = nego_buyer.build_bargain_init(details)
        nego_seller.check_bargain_init(init_msg)

        output = [{
            'amount': self.product.initial_price,
            'script': address_to_script(self.get_seller_address())
        }]
        details = BargainRequestDetails(
            int(time.time()),
            output,
            expires=int(time.time()) + 3600,
        )
        request_msg = nego_seller.build_bargain_request(details)
        nego_buyer.check_bargain_request(request_msg)

        self.nego_buyer = pickle.dumps(nego_buyer)
        self.nego_seller = pickle.dumps(nego_seller)
