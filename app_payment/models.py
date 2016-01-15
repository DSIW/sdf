# coding=utf-8

from django.db import models

from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator

from django.forms import ModelForm

from paypal.standard.models import *
from paypal.standard.ipn.models import PayPalIPN

import uuid

# Create your models here.
class Payment(models.Model):
    book = models.ForeignKey('app_book.Book') # don't import Book for circular import
    seller_user = models.ForeignKey('app_user.User', related_name='seller_user')
    buyer_user = models.ForeignKey('app_user.User', related_name='buyer_user')
    last_ipn = models.ForeignKey(PayPalIPN, null=True)

    item_name = models.CharField(max_length=255)
    amount = models.FloatField(default=0.0)
    quantity = models.IntegerField(1)
    invoice = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=255)

    business = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    custom = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    def init_process(self, offer, user, source):
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
        self.source = source

    def save(self, *args, **kwargs):
        ''' On save, update created_at '''
        if not self.id:
            self.created_at = datetime.now()
        return super(Payment, self).save(*args, **kwargs)

    def is_active(self):
        return self.payment_status in [ST_PP_CREATED, ST_PP_ACTIVE, ST_PP_PENDING, ST_PP_VOIDED]

    def is_cancelled(self):
        return self.payment_status == ST_PP_CANCELLED

    def is_completed(self):
        return self.payment_status == ST_PP_COMPLETED

    def last_valid_time(self):
        return self.created_at + timedelta(seconds=settings.UNPAID_PAYMENT_TIMEOUT)

    def __str__(self):
        return self.buyer_user.full_name() + " buyes " + self.book.name + " from " + self.seller_user.full_name()

class SellerRating(models.Model):
     payment = models.ForeignKey(Payment,related_name='rated_payment')
     rating_user = models.ForeignKey('app_user.User',related_name='rating_buyer')
     rated_user = models.ForeignKey('app_user.User',related_name='rated_seller')
     rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
     textrating = models.CharField(max_length=200, blank=True)
     updatedAt  = models.DateField('updated_at')
     createdAt  = models.DateField('created_at')
     def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
        return super(SellerRating, self).save(*args, **kwargs)

     class Meta:
        unique_together = ('rating_user','rated_user',"payment")

     def full_stars(self):
        return self.rating
     def empty_stars(self):
        return 5-self.rating

     @staticmethod
     def calculate_stars_for_user(id):
        user_ratings = SellerRating.objects.filter(rated_user_id = id)
        rating = 0
        full_stars = 0
        has_halfstar = False
        empty_stars = 5
        i = 0
        if user_ratings:
            for user_rating in user_ratings:
                rating += user_rating.rating
                i=i+1
            rating = rating / i
            full_stars = rating - (rating % 1)
            empty_stars = 5 - full_stars
            if full_stars < 5:
                if rating > full_stars:
                    has_halfstar = True
                if has_halfstar:
                    empty_stars = empty_stars -1

        return {'rating':rating, 'rating_count':i, 'full_stars':int(full_stars),'has_halfstar':has_halfstar,'empty_stars':int(empty_stars)}
