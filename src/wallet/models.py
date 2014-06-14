from django.db import models
from django.contrib.auth.models import User


class WalletManager(models.Manager):
    def get_for_user(self, user):
        return self.get(user=user)


class Wallet(models.Model):
    objects = WalletManager()

    user = models.ForeignKey(User, related_name='wallet')
    privkey = models.CharField(max_length=32)
    pubkey = models.CharField(max_length=200)
    amount = models.PositiveIntegerField(default=0)
