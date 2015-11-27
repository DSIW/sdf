# coding=utf-8

from django.db import models

import json
from datetime import datetime

from app_user.models import User
from paypal.standard.models import *
from paypal.standard.ipn.models import PayPalIPN

# Create your models here.
class Payment(models.Model):
    book = models.ForeignKey('app_book.Book') # don't import Book for circular import
    seller_user = models.ForeignKey(User, related_name='seller_user')
    buyer_user = models.ForeignKey(User, related_name='buyer_user')
    last_ipn = models.ForeignKey(PayPalIPN, null=True)

    item_name = models.CharField(max_length=255)
    amount = models.FloatField(default=0.0)
    quantity = models.IntegerField(1)
    invoice = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=255)

    business = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    custom = models.CharField(max_length=255)

    def init_process(self, offer, user):
        self.book = offer.book
        self.seller_user = self.book.offer().seller_user
        self.buyer_user = user
        self.quantity = 1
        self.business = self.seller_user.paypal
        self.payment_status = ST_PP_VOIDED
        self.amount = offer.totalPrice()
        self.item_name = self.book.name + ' von ' + self.book.author
        self.currency_code = 'EUR'
        self.invoice = datetime.now().strftime('%Y%m%d-%H%M%S')+"-book-"+str(self.book.id)+"-seller-"+str(self.seller_user.id)

        self.save() # get id for custom JSON
        self.custom = json.dumps({'payment_id': self.id})

    def __str__(self):
        return self.buyer_user.full_name() + " buyes " + self.book.name + " from " + self.seller_user.full_name()
