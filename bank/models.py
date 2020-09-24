from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import random


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.IntegerField(
        verbose_name="Account number", default=random.randint(100, 1000))
    account_balance = models.IntegerField(default=100)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Transaction(models.Model):
    types = [
        ('Deposit', "DEPOSIT"),
        ('Withdraw', "WITHDRAW")
    ]

    account = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=20, default="N/A")
    trans_date = models.DateTimeField(default=timezone.now)
    trans_type = models.CharField(
        verbose_name="Transaction Type", max_length=20, choices=types, default="Deposit")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("bank:profile")

    def save(self, *args, **kwargs):
        if self.trans_type == 'Withdraw':
            self.account.profile.account_balance -= self.amount
        else:
            self.account.profile.account_balance += self.amount
        self.account.save()
        # Call the real save() method
        super(Transaction, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.account.profile.account_balance -= self.amount
        self.account.save()
        super(Transaction, self).delete(*args, **kwargs)
