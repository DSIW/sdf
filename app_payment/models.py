# coding=utf-8

from django.db import models

import json
from datetime import datetime

from app_user.models import User
from app_book.models import Book
from paypal.standard.models import *
from paypal.standard.ipn.models import PayPalIPN

# Create your models here.
class Payment(models.Model):
    book = models.ForeignKey(Book)
    receiver_user = models.ForeignKey(User, related_name='receiver_user')
    payer_user = models.ForeignKey(User, related_name='payer_user')
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
        book = offer.book
        seller = book.user
        buyer = User.objects.filter(id=user.id).first()

        self.book = book
        self.receiver_user = User.objects.filter(id=seller.id).first()
        self.payer_user = buyer
        self.quantity = 1
        self.business = seller.paypal
        self.payment_status = ST_PP_VOIDED
        self.amount = offer.totalPrice()
        self.item_name = book.name + ' von ' + book.author
        self.currency_code = 'EUR'
        self.invoice = datetime.now().strftime('%Y%m%d-%H%M%S')+"-book-"+str(book.id)+"-seller-"+str(user.id)

        self.save() # get id for custom JSON
        self.custom = json.dumps({'payment_id': self.id})


    def init(self):
        # add book payment status
        # hide book via is_in_payment_process
        # show book for buyer and seller
        pass

    def complete(self):
        self.payment_status = ST_PP_COMPLETED
        # remove book payment status
        # move book to buyer
        # remove book from showcase
        pass

    def abort(self):
        # remove book payment status
        # readd book to showcase
        pass

    def update_from_paypal_ipn(self, paypal_ipn):
        self.payment_status = paypal_ipn.payment_status
        self.last_ipn = paypal_ipn


    def __str__(self):
        return self.payer_user.full_name() + " buyes " + self.book.name + " from " + self.receiver_user.full_name()
