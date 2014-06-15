import pickle
import time

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from pybazaar_protocol.negotiation import Negotiation
from pybazaar_protocol.messages import (
    BargainInitDetails, BargainRequestDetails, BargainProposalDetails,
    BargainProposalAckDetails, SIGN_ECDSA_SHA256
)
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
        wallet = Wallet.objects.get_for_user(self.product.owner)

        nego_buyer = Negotiation(role=Negotiation.ROLE_BUYER)
        nego_seller = Negotiation(role=Negotiation.ROLE_SELLER)

        details = BargainInitDetails('', '')
        init_msg = nego_buyer.build_bargain_init(details)
        nego_seller.check_bargain_init(init_msg)

        output = [{
            'amount': self.product.initial_price,
            'script': address_to_script(wallet.address)
        }]
        details = BargainRequestDetails(
            int(time.time()),
            output,
            expires=int(time.time()) + 3600,
            memo='Hello! Do you want to buy my wonderful product?',
        )
        request_msg = nego_seller.build_bargain_request(details)
        nego_buyer.check_bargain_request(request_msg)

        self.nego_buyer = pickle.dumps(nego_buyer)
        self.nego_seller = pickle.dumps(nego_seller)

    def create_message(self, user, price, memo):
        if user == self.buyer:
            self.create_buyer_message(price, memo)
        else:
            self.create_seller_message(price, memo)

    def create_buyer_message(self, price, memo):
        wallet = Wallet.objects.get_for_user(self.buyer)
        inputs = [{
            'output': u'6317c147efc54f1c0291cd5cc403db289c5228d054f0cf2ff91265c480efd385:0',
            'value': price,
            'address': wallet.address,
            'privkey': wallet.privkey
        }]
        nego_buyer = pickle.loads(self.nego_buyer)
        last_msg = nego_buyer.get_last_message_received()
        refund_to = [{'script': address_to_script(wallet.address)}]
        details = BargainProposalDetails(
            inputs,
            last_msg.details.outputs,
            price,
            refund_to,
            [],
            memo.encode(),
            '',
            ''
        )
        msg = nego_buyer.build_bargain_proposal(
            details,
            SIGN_ECDSA_SHA256,
            wallet.pubkey.encode(),
            wallet.privkey
        )

        nego_seller = pickle.loads(self.nego_seller)
        nego_seller.check_bargain_proposal(msg)

        self.nego_buyer = pickle.dumps(nego_buyer)
        self.nego_seller = pickle.dumps(nego_seller)
        self.save()

    def create_seller_message(self, price, memo):
        wallet = Wallet.objects.get_for_user(self.product.owner)
        output = [{
            'amount': price,
            'script': address_to_script(wallet.address)
        }]
        details = BargainProposalAckDetails(
            output,
            memo,
            '', ''
        )
        nego_seller = pickle.loads(self.nego_seller)
        msg = nego_seller.build_bargain_proposal_ack(
            details,
            SIGN_ECDSA_SHA256,
            wallet.pubkey,
            wallet.privkey
        )

        nego_buyer = pickle.loads(self.nego_buyer)
        nego_buyer.check_bargain_proposal_ack(msg)

        self.nego_buyer = pickle.dumps(nego_buyer)
        self.nego_seller = pickle.dumps(nego_seller)
        self.save()
