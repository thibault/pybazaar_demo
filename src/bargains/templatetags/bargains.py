from django import template
from pybazaar_protocol.messages import (
    TYPE_BARGAIN_REQUEST, TYPE_BARGAIN_PROPOSAL, TYPE_BARGAIN_PROPOSAL_ACK)

register = template.Library()


@register.simple_tag
def bargain_author(user, bargain, message):
    if message.message_type == TYPE_BARGAIN_PROPOSAL:
        is_author = (user == bargain.buyer)
    else:
        is_author = (user != bargain.buyer)

    return 'You:' if is_author else 'The other:'
