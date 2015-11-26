# -*- coding: utf-8 -*-

from django.db import models

from app_user.models import User
from app_payment.models import Payment
from paypal.standard.models import *

ACTIVE_PAYMENT_STATUSES = [ST_PP_CREATED, ST_PP_ACTIVE, ST_PP_PENDING, ST_PP_VOIDED]

class Book(models.Model):
    user = models.ForeignKey(User, default=None)

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    language = models.CharField(max_length=100)
    releaseDate = models.DateField('release_date')
    pageNumber = models.IntegerField(default=0)
    isbn10 = models.CharField(max_length=100)
    isbn13 = models.CharField(max_length=100)
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name + ", " + self.author + " (" + self.language + ", " + str(self.releaseDate) + ")"

    def is_published(self):
        return self.offer_set.count() > 0 and self.offer_set.first().active

    def price(self):
        if self.offer() is None:
            return 0.0
        return self.offer().price

    def shipping_price(self):
        if self.offer() is None:
            return 0.0
        return self.offer().shipping_price

    def total_price(self):
        if self.offer() is None:
            return 0.0
        return self.offer().totalPrice()

    def offer(self):
        return self.offer_set.first()


class Offer(models.Model):
    seller_user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    price = models.FloatField()
    shipping_price = models.FloatField()
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ("seller_user", "book")

    def __str__(self):
        return "" + str(self.seller_user.pseudonym_or_full_name()) + ", <Book: " + str(self.book) + ">, " + str(self.price) + ", " + str(self.shipping_price)

    def totalPrice(self):
        return self.price + self.shipping_price

    def active_counteroffers(self):
        return self.counteroffer_set.filter(offer=self, active=True).count()

    def is_in_active_payment_process(self):
        return Payment.objects.filter(book=self.book, payment_status__in=ACTIVE_PAYMENT_STATUSES).count() > 0


class Counteroffer(models.Model):
    offer = models.ForeignKey(Offer)
    creator = models.ForeignKey(User)
    price = models.FloatField(default=0)
    active = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)

    def accept(self):
        if self.active:
            self.accepted=True
            self.active=False
            self.save()
        else:
            raise BaseException("Counteroffer is not active anymore")

    def decline(self):
        if self.active:
            self.accepted=False
            self.active=False
            self.save()
        else:
            raise BaseException("Counteroffer is not active anymore")

    def __str__(self):
        return "Counteroffer: <offer_PK: " + str(self.offer.primary_key) + ">, <user_PK: " + str(self.creator.primary_key) + ">, <price: " + self.price + ">"

