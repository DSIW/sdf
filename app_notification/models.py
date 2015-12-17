# coding=utf-8
from django.db import models
from app_user.models import User
from app_book.models import Book, Offer, Counteroffer
from app_payment.models import Payment
from datetime import datetime
from django.shortcuts import get_object_or_404

from app.templatetags import template_extras

class Notification(models.Model):
    FASTBUY = 'FASTBUY'  # Empfdaenger bekommt Notification => Subject: Buch X wurde gekauft | Nachricht: Person X hat NBuch Y gekauft
    ABORT_PAYMENT = 'ABORT_PAYMENT'
    COUNTEROFFER = 'COUNTEROFFER'  # Verkaeufer bekommt Nachricht => Subject: Person Y hat fuer Buch X ein Angebot gemacht | Nachricht: Person Y hat fuer Buch X ein Angebot gemacht so und soviel Euro => Annehmen | Ablehnen -> CounterOffer Id
    COUNTEROFFER_ACCEPT = 'COUNTEROFFER_ACCEPT'  # Kaeufer bekommt Nachricht: Subject: Preisvorscvhlag fuer Buch X wurde akzeptiert | Nachricht: Fuer das Buch X wurde Preisvorschlag akzeptiert
    COUNTEROFFER_DECLINE = 'COUNTEROFFER_DECLINE'  # Kaeufer bekommt Nachricht: Subject: Preisvorscvhlag fuer Buch X wurde nicht akzeptiert | Nachricht: Fuer das Buch X wurde Preisvorschlag nicht akzeptiert
    BOOK_SEND = 'BOOK_SEND' # Buch versendet
    REQUEST_RATING = 'REQUEST_RATING' # Den Verkäufer nach Erhalt des Buches bewerten.
    NOTIFICATION_TYPE = (
        (FASTBUY, 'Sofortkauf'),
        (ABORT_PAYMENT, 'Zahlungsabbruch'),
        (COUNTEROFFER, 'Preisvorschlag'),
        (COUNTEROFFER_ACCEPT, 'Preisvorschlag akzeptiert'),
        (COUNTEROFFER_DECLINE, 'Preisvorschlag abgelehnt'),
        (BOOK_SEND, 'Buch verschickt'),
        (REQUEST_RATING, 'Verkäufer bewerten'),
    )

    sender_user = models.ForeignKey(User, related_name='sender_user', default=None)
    receiver_user = models.ForeignKey(User, related_name='receiver_user', default=None)
    message = models.TextField(max_length=1500)
    subject = models.CharField(max_length=200)
    received_date = models.DateTimeField('received_date')
    counter_offer = models.ForeignKey(Counteroffer, default=None, null=True, blank=True)
    payment = models.ForeignKey(Payment, default=None, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    notification_type = models.CharField(max_length=200,
                                         choices=NOTIFICATION_TYPE,
                                         default=FASTBUY)

    @staticmethod
    def fastbuy(buyer, seller, book):
        subject = 'Verkauf von "' + book.name + '"'
        msg = 'Der Benutzer ' + buyer.full_name() + ' hat Ihr Buch '+book.name+' gekauft.'

        notification = Notification(
            sender_user = buyer,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.FASTBUY,
            receiver_user=seller,
            offer=book.offer
        )

        notification.save()

    @staticmethod
    def abort_unpaid_payment(payment):
        book = payment.book
        subject = 'Kauf von "' + book.name + '" wurde abgebrochen'
        msg = 'Das System hat Ihren Kauf von Buch '+book.name+' abgebrochen, da Sie mehr als 30 Minuten keine Zahlung getätigt haben.'

        notification = Notification(
            sender_user = payment.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.ABORT_PAYMENT,
            receiver_user=payment.buyer_user
        )

        notification.save()

    @staticmethod
    def counteroffer(counteroffer, seller, buyer, book):
        subject = 'Neuer Preisvorschlag für das Buch ' + book.name
        msg = 'Der Benutzer ' + buyer.full_name() + ' möchte das Buch "'+book.name+'" für '+template_extras.currency(counteroffer.price)+' kaufen.'

        notification = Notification(
            sender_user = buyer,
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
            sender_user = counteroffer.offer.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.COUNTEROFFER_DECLINE,
            receiver_user=buyer,
            counter_offer=counteroffer
        )

        notification.save()

    @staticmethod
    def counteroffer_accept(counteroffer, buyer, book, payment):
        # Preisvorschlag akzeptiert
        subject = 'Preisvorschlag für das Buch ' + book.name + ' wurde akzeptiert.'
        msg = 'Der von Ihnen vorgeschlagene Preis für das Buch: "' + book.name + '" in  Höhe von ' + template_extras.currency(counteroffer.price) + ' wurde von dem Verkäufer akzeptiert.'

        notification = Notification(
            sender_user = counteroffer.offer.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.COUNTEROFFER_ACCEPT,
            receiver_user=buyer,
            counter_offer=counteroffer,
            payment=payment
        )

        notification.save()

    def __str__(self):
        return self.subject + ", " + self.message


    @staticmethod
    def send_book(notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        notification.notification_type = Notification.BOOK_SEND
        notification.save()

        counteroffer = get_object_or_404(Counteroffer, id=notification.counter_offer.id)
        buyer = get_object_or_404(User, id=counteroffer.creator.id)
        offer = get_object_or_404(Offer, id=counteroffer.offer.id)
        book = get_object_or_404(Book, id=offer.book.id)

        # Buchversand bestaetigt
        subject = 'Das Buch ' + book.name + ' wurde verschickt.'
        msg = 'Der Verkäufer hat bestätigt das er das Buch: "' + book.name + '" zu Ihnen versendet hat.'

        new_notification = Notification(
            sender_user = offer.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.BOOK_SEND,
            receiver_user=buyer
        )

        new_notification.save()

    def __str__(self):
        return self.subject + ", " + self.message

    @staticmethod
    def request_rating(payment):
        seller_name = payment.seller_user.pseudonym_or_full_name()
        subject = 'Bewerten Sie '+seller_name+'!'
        msg = 'Sie haben ein Buch von '+seller_name+' gekauft. Der Verkäufer würde sich über eine Bewertung freuen!'
        new_notification = Notification(
            sender_user = payment.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.REQUEST_RATING,
            payment=payment,
            receiver_user=payment.buyer_user)
        new_notification.save()
