# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Max

from app_user.models import User
from sdf.base_settings import *
from app_payment.models import Payment
from paypal.standard.models import *
import glob
import isbnlib

ACTIVE_PAYMENT_STATUSES = [ST_PP_CREATED, ST_PP_ACTIVE, ST_PP_PENDING, ST_PP_VOIDED]

def book_directory_path(instance, filename):
    if instance.id is None:
        id_max = Book.objects.all().aggregate(Max('id'))['id__max']
        id_next = id_max + 1 if id_max else 1
        instance.id = id_next
    ext = filename.split('.')[-1]
    upload_dir_path = 'images/books/book_{0}.{1}'.format(instance.id, ext)
    book_images = glob.glob(os.path.join(MEDIA_ROOT, 'images/books/book_{0}.*'.format(instance.id)))
    for image in book_images:
        os.remove(image)
    return upload_dir_path

def validate_isbn10(value):
      if not isbnlib.is_isbn10(value):
          raise ValidationError('%s ist keine ISBN-10 Nummer' % value)

def validate_isbn13(value):
      if not isbnlib.is_isbn13(value):
          raise ValidationError('%s ist keine ISBN-13 Nummer' % value)

class Book(models.Model):
    user = models.ForeignKey(User, default=None)

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    language = models.CharField(max_length=100)
    releaseDate = models.DateField('release_date')
    pageNumber = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(9999)])
    isbn10 = models.CharField(blank=True, max_length=100, validators=[validate_isbn10])
    isbn13 = models.CharField(blank=True, max_length=100, validators=[validate_isbn13])
    image = models.FileField(help_text='max. 42 megabytes', upload_to=book_directory_path, null=False, default='images/books/book-cover-default.jpg', blank=True)
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name + ", " + self.author + " (" + self.language + ", " + str(self.releaseDate) + ")"

    def is_published(self):
        return self.offer_set.count() > 0 and self.offer_set.first().active

    def is_private(self):
        return not self.is_published()

    def price(self):
        if self.is_private():
            return 0.0
        return self.offer().price

    def shipping_price(self):
        if self.is_private():
            return 0.0
        return self.offer().shipping_price

    def total_price(self):
        if self.is_private():
            return 0.0
        return self.offer().totalPrice()

    def offer(self):
        return self.offer_set.first()

    def active_payment(self):
        return Payment.objects.filter(book=self, payment_status__in=ACTIVE_PAYMENT_STATUSES).first()

    def is_in_active_payment_process(self):
        return self.active_payment() is not None


class Offer(models.Model):
    updated = models.DateTimeField(auto_now=True)
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

    def highest_counteroffer_price(self):
        return Counteroffer.objects.filter(offer=self, active=True).order_by('price').last().price


class Counteroffer(models.Model):
    offer = models.ForeignKey(Offer)
    creator = models.ForeignKey(User)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.01)])
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
        return "Counteroffer: <offer_PK: " + str(self.offer.id) + ">, <user_PK: " + str(self.creator.id) + ">, <price: " + str(self.price) + ">"

