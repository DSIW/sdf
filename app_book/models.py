# -*- coding: utf-8 -*-

from django.db import models

from app_user.models import User
from sdf.base_settings import *
import glob

def book_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    upload_dir_path = 'images/books/book_{0}.{1}'.format(instance.id, ext)
    book_images = glob.glob(os.path.join(MEDIA_ROOT, 'images/books/book_{0}.*'.format(instance.id)))
    for image in book_images:
        os.remove(image)
    return upload_dir_path

class Book(models.Model):
    user = models.ForeignKey(User, default=None)

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    language = models.CharField(max_length=100)
    releaseDate = models.DateField('release_date')
    pageNumber = models.IntegerField(default=0)
    isbn10 = models.CharField(max_length=100)
    isbn13 = models.CharField(max_length=100)
    image = models.FileField(help_text='max. 42 megabytes', upload_to=book_directory_path, default='')
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name + ", " + self.author + " (" + self.language + ", " + str(self.releaseDate) + ")"

    def is_published(self):
        return self.offer_set.count() > 0 and self.offer_set.first().active


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

