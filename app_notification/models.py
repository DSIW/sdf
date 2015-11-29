# coding=utf-8
from django.db import models
from app_user.models import User
from app_book.models import Counteroffer
from datetime import datetime

from app.templatetags import template_extras

# Create your models here.

class Notification(models.Model):
    FASTBUY = 'FASTBUY'  # Empfdaenger bekommt Notification => Subject: Buch X wurde gekauft | Nachricht: Person X hat NBuch Y gekauft
    COUNTEROFFER = 'COUNTEROFFER'  # Verkaeufer bekommt Nachricht => Subject: Person Y hat fuer Buch X ein Angebot gemacht | Nachricht: Person Y hat fuer Buch X ein Angebot gemacht so und soviel Euro => Annehmen | Ablehnen -> CounterOffer Id
    COUNTEROFFER_ACCEPT = 'COUNTEROFFER_ACCEPT'  # Kaeufer bekommt Nachricht: Subject: Preisvorscvhlag fuer Buch X wurde akzeptiert | Nachricht: Fuer das Buch X wurde Preisvorschlag akzeptiert
    COUNTEROFFER_DECLINE = 'COUNTEROFFER_DECLINE'  # Kaeufer bekommt Nachricht: Subject: Preisvorscvhlag fuer Buch X wurde nicht akzeptiert | Nachricht: Fuer das Buch X wurde Preisvorschlag nicht akzeptiert
    NOTIFICATION_TYPE = (
        (FASTBUY, 'Sofortkauf'),
        (COUNTEROFFER, 'Preisvorschlag'),
        (COUNTEROFFER_ACCEPT, 'Preisvorschlag akzeptiert'),
        (COUNTEROFFER_DECLINE, 'Preisvorschlag abgelehnt'),
    )

    receiver_user = models.ForeignKey(User, default=None)
    message = models.TextField(max_length=1500)
    subject = models.CharField(max_length=200)
    received_date = models.DateTimeField('received_date')
    counter_offer = models.OneToOneField(Counteroffer, default=None, null=True, blank=True)
    notification_type = models.CharField(max_length=200,
                                         choices=NOTIFICATION_TYPE,
                                         default=FASTBUY)

    @staticmethod
    def fastbuy(buyer, seller, book):
        subject = 'Buch ' + book.name + ' wurde gekauft'
        msg = 'Das von Ihnen zum Verkauf gestellte Buch: "' + book.name + '" wurde verkauft. Der Benutzer ' + buyer.full_name() + ' hat das Buch gekauft'

        notification = Notification(
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.FASTBUY,
            receiver_user=seller
        )

        notification.save()

    @staticmethod
    def counteroffer(counteroffer, seller, buyer, book):
        subject = 'Neuer Preisvorschlag für das Buch ' + book.name
        msg = 'Der Benutzer ' + buyer.full_name() + ' möchte das Buch "'+book.name+'" für '+template_extras.currency(counteroffer.price)+' kaufen.'

        notification = Notification(
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.COUNTEROFFER,
            receiver_user=seller,
            counter_offer=counteroffer
        )

        notification.save()

    @staticmethod
    def counteroffer_decline(counteroffer, buyer, book):
        # Preisvorschlag nicht akzeptiert
        subject = 'Preisvorschlag für das Buch "' + book.name + '" wurde nicht akzeptiert.'
        msg = 'Der von Ihnen vorgeschlagene Preis für das Buch "' + book.name + '" in  Höhe von ' + template_extras.currency(counteroffer.price) + ' wurde von dem Verkäufer nicht akzeptiert.'

        notification = Notification(
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.COUNTEROFFER_DECLINE,
            receiver_user=buyer
        )

        notification.save()

    @staticmethod
    def counteroffer_accept(counteroffer, buyer, book):
        # Preisvorschlag akzeptiert
        subject = 'Preisvorschlag für das Buch ' + book.name + ' wurde akzeptiert.'
        msg = 'Der von Ihnen vorgeschlagene Preis für das Buch: "' + book.name + '" in  Höhe von ' + str(counteroffer.price) + ' wurde von dem Verkäufer akzeptiert.'

        notification = Notification(
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.COUNTEROFFER_ACCEPT,
            receiver_user=buyer
        )

        notification.save()

    def __str__(self):
        return self.subject + ", " + self.message