# coding=utf-8
import threading

from django.core.mail import send_mail
from django.db import models
from app_user.models import User, ChangeUserData
from app_book.models import Book, Offer, Counteroffer
from app_payment.models import Payment
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from app.templatetags import template_extras
from django.conf import settings


class Notification(models.Model):
    FASTBUY = 'FASTBUY'  # Empfdaenger bekommt Notification => Subject: Buch X wurde gekauft | Nachricht: Person X hat NBuch Y gekauft
    ABORT_PAYMENT = 'ABORT_PAYMENT'
    COUNTEROFFER = 'COUNTEROFFER'  # Verkaeufer bekommt Nachricht => Subject: Person Y hat fuer Buch X ein Angebot gemacht | Nachricht: Person Y hat fuer Buch X ein Angebot gemacht so und soviel Euro => Annehmen | Ablehnen -> CounterOffer Id
    COUNTEROFFER_ACCEPT = 'COUNTEROFFER_ACCEPT'  # Kaeufer bekommt Nachricht: Subject: Preisvorscvhlag fuer Buch X wurde akzeptiert | Nachricht: Fuer das Buch X wurde Preisvorschlag akzeptiert
    COUNTEROFFER_DECLINE = 'COUNTEROFFER_DECLINE'  # Kaeufer bekommt Nachricht: Subject: Preisvorscvhlag fuer Buch X wurde nicht akzeptiert | Nachricht: Fuer das Buch X wurde Preisvorschlag nicht akzeptiert
    BOOK_SEND = 'BOOK_SEND' # Buch versendet
    REQUEST_RATING = 'REQUEST_RATING' # Den Verkäufer nach Erhalt des Buches bewerten.
    CHANGE_PROFILE_ADMIN = 'CHANGE_PROFILE_ADMIN' # Notification fuer den Administrator wenn ein Antrag auf aendern des Benutzerprofils gestellt wurde
    CHANGE_PROFILE_CUSTOMER= 'CHANGE_PROFILE_CUSTOMER' # Notification fuer den Kunden wenn ein Antrag auf aendern des Benutzerprofils angenommen / abgelehnt wurde
    REMOVE_PROFILE_ADMIN = 'REMOVE_PROFILE_ADMIN' # Notification fuer den Administrator wenn ein Antrag auf Loeschung des Benutzerprofils gestellt wurde
    BANN_UNBANN_USER = 'BANN_UNBANN_USER' # Notification fuer den User wenn er gesperrt/entsperrt wurde
    NOTIFICATION_TYPE = (
        (FASTBUY, 'Sofortkauf'),
        (ABORT_PAYMENT, 'Zahlungsabbruch'),
        (COUNTEROFFER, 'Preisvorschlag'),
        (COUNTEROFFER_ACCEPT, 'Preisvorschlag akzeptiert'),
        (COUNTEROFFER_DECLINE, 'Preisvorschlag abgelehnt'),
        (BOOK_SEND, 'Buch verschickt'),
        (REQUEST_RATING, 'Verkäufer bewerten'),
        (CHANGE_PROFILE_ADMIN, 'Antrag ändern des Nutzerprofils Administrator'),
        (CHANGE_PROFILE_CUSTOMER, 'Antrag angenommen / abgelehnt ändern des Nutzerprofils Kunde'),
        (REMOVE_PROFILE_ADMIN, 'Antrag Löschung des Nutzerprofils '),
        (BANN_UNBANN_USER, '(Ent-)Sperrung des Nutzerprofils '),
    )

    sender_user = models.ForeignKey(User, related_name='sender_user', default=None)
    receiver_user = models.ForeignKey(User, related_name='receiver_user', default=None)
    message = models.TextField(max_length=1500)
    subject = models.CharField(max_length=200)
    received_date = models.DateTimeField('received_date')
    counter_offer = models.ForeignKey(Counteroffer, default=None, null=True, blank=True)
    book = models.ForeignKey(Book, default=None, null=True, blank=True)
    payment = models.ForeignKey(Payment, default=None, null=True, blank=True)
    change_user_profile = models.ForeignKey(ChangeUserData, default=None, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    notification_type = models.CharField(max_length=200,
                                         choices=NOTIFICATION_TYPE,
                                         default=FASTBUY)

    @staticmethod
    def fastbuy(buyer, seller, book):
        subject = 'Verkauf von "' + book.name + '"'
        msg = 'Der Benutzer ' + buyer.full_name() + ' hat Ihr Buch '+book.name+' gekauft.'

        notification = Notification(
            sender_user=buyer,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.FASTBUY,
            receiver_user=seller,
            book=book
        )

        notification.save()
        NotificationEmailThread(notification.receiver_user, notification.subject, notification.message).start()

    @staticmethod
    def abort_unpaid_payment(payment):
        book = payment.book
        subject = 'Kauf von "' + book.name + '" wurde abgebrochen'
        msg = 'Das System hat Ihren Kauf von Buch '+book.name+' abgebrochen, da Sie mehr als 30 Minuten keine Zahlung getätigt haben.'

        notification = Notification(
            sender_user=payment.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.ABORT_PAYMENT,
            receiver_user=payment.buyer_user,
            book=book
        )

        notification.save()
        NotificationEmailThread(notification.receiver_user, notification.subject, notification.message).start()

    @staticmethod
    def counteroffer(counteroffer, seller, buyer, book):
        subject = 'Neuer Preisvorschlag für das Buch ' + book.name
        msg = 'Der Benutzer ' + buyer.full_name() + ' möchte das Buch "'+book.name+'" für '+template_extras.currency(counteroffer.price)+' kaufen.'

        notification = Notification(
            sender_user=buyer,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.COUNTEROFFER,
            receiver_user=seller,
            counter_offer=counteroffer,
            book=book
        )

        notification.save()
        NotificationEmailThread(notification.receiver_user, notification.subject, notification.message).start()

    @staticmethod
    def counteroffer_decline(counteroffer, buyer, book):
        # Preisvorschlag nicht akzeptiert
        subject = 'Preisvorschlag für das Buch "' + book.name + '" wurde nicht akzeptiert.'
        msg = 'Der von Ihnen vorgeschlagene Preis für das Buch "' + book.name + '" in  Höhe von ' + template_extras.currency(counteroffer.price) + ' wurde von dem Verkäufer nicht akzeptiert.'

        notification = Notification(
            sender_user=counteroffer.offer.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.COUNTEROFFER_DECLINE,
            receiver_user=buyer,
            counter_offer=counteroffer,
            book=book
        )

        notification.save()
        NotificationEmailThread(notification.receiver_user, notification.subject, notification.message).start()

    @staticmethod
    def counteroffer_accept(counteroffer, buyer, book, payment):
        # Preisvorschlag akzeptiert
        subject = 'Preisvorschlag für das Buch ' + book.name + ' wurde akzeptiert.'
        msg = 'Der von Ihnen vorgeschlagene Preis für das Buch: "' + book.name + '" in  Höhe von ' + template_extras.currency(counteroffer.price) + ' wurde von dem Verkäufer akzeptiert.'

        notification = Notification(
            sender_user=counteroffer.offer.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.COUNTEROFFER_ACCEPT,
            receiver_user=buyer,
            counter_offer=counteroffer,
            payment=payment,
            book=book
        )

        notification.save()
        NotificationEmailThread(notification.receiver_user, notification.subject, notification.message).start()


    def __str__(self):
        return self.subject + ", " + self.message


    @staticmethod
    def send_book(notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        notification.notification_type = Notification.BOOK_SEND
        notification.save()

        buyer = get_object_or_404(User, id=notification.sender_user.id)
        seller = get_object_or_404(User, id=notification.receiver_user.id)
        book = get_object_or_404(Book, id=notification.book.id)
        payment = Payment.objects.filter(book=book).last()

        payment.shipped = True
        payment.save()

        # Buchversand bestaetigt
        subject = 'Das Buch ' + book.name + ' wurde verschickt.'
        msg = 'Der Verkäufer hat bestätigt, dass er das Buch "' + book.name + '" zu Ihnen versendet hat.'

        new_notification = Notification(
            sender_user=seller,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.BOOK_SEND,
            receiver_user=buyer,
            book=book
        )

        new_notification.save()
        NotificationEmailThread(new_notification.receiver_user, new_notification.subject, new_notification.message).start()


    def __str__(self):
        return self.subject + ", " + self.message

    @staticmethod
    def request_rating(payment):
        seller_name = payment.seller_user.pseudonym_or_full_name()
        subject = 'Bewerten Sie '+seller_name+'!'
        msg = 'Sie haben ein Buch von '+seller_name+' gekauft. Der Verkäufer würde sich über eine Bewertung freuen!'
        new_notification = Notification(
            sender_user=payment.seller_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.REQUEST_RATING,
            payment=payment,
            receiver_user=payment.buyer_user)
        new_notification.save()
        NotificationEmailThread(new_notification.receiver_user, new_notification.subject, new_notification.message).start()

    @staticmethod
    def request_change_userprofile_administrator(customer_user_id, changeUserData):
        '''Diese Methode erstellt eine Notification wenn ein Kunde einen Antrag auf Datenaenderung erstellt
        Diese Notification geht an alle Benutzer welche den Flag is_staff innehaben
        '''
        admins = User.objects.filter(is_staff = True)
        customer_user = get_object_or_404(User, id=customer_user_id)

        msg = 'Der Kunde ' + customer_user.pseudonym_or_full_name() + ' hat einen Antrag auf Datenänderung gestellt. Folgende Daten möchte der Kunde aktualisiert haben: <br>'
        if (changeUserData.first_name+changeUserData.last_name) != (customer_user.first_name+customer_user.last_name):
            msg += 'Klarname: ' + changeUserData.first_name + ' ' + changeUserData.last_name + ' (vorher: ' + customer_user.first_name + ' ' + customer_user.last_name + ')<br>'
        if changeUserData.username is not None:
            if changeUserData.username != customer_user.username:
                msg += 'Pseudonym: ' + changeUserData.username + ' (vorher: ' + str(customer_user.username) + ') <br>'
        elif customer_user.username is not None:
            msg += 'Das Pseudonym soll gelöscht werden. (vorher: ' + str(customer_user.username) + ') <br>'
        if changeUserData.email != customer_user.email:
            msg += 'E-Mail Adresse: ' + changeUserData.email + ' (vorher: ' + customer_user.email + ') <br>'
        if changeUserData.location != customer_user.location:
            msg += 'Wohnort: ' + changeUserData.location + ' (vorher: ' + customer_user.location + ') <br>'
        if changeUserData.paypal != customer_user.paypal:
            msg += 'Paypal Adresse: ' + changeUserData.paypal + ' (vorher: ' + customer_user.paypal + ') <br>'

        for admin in admins:
            subject = 'Antrag auf Datenänderung'

            new_notification = Notification(
                sender_user=customer_user,
                subject=subject,
                message=msg,
                received_date=datetime.now(),
                notification_type=Notification.CHANGE_PROFILE_ADMIN,
                change_user_profile=changeUserData,
                receiver_user=admin)
            new_notification.save()
            NotificationEmailThread(new_notification.receiver_user, new_notification.subject, 'Nutzer möchte Profildaten geändert haben.').start()

    @staticmethod
    def request_change_userprofile_customer(admin_user_id, customer_user_id, accepted):
        '''Diese Methode erstellt eine Notification wenn ein ein Antrag auf Datenaenderung akzeptiert / abgelehnt wurde
        Diese Notification geht an den Kunde welcher die Anfrage erstellt hat
        '''
        customer_user = get_object_or_404(User, id=customer_user_id)
        admin_user = get_object_or_404(User, id=admin_user_id)

        user_data = '<br>Klarname: ' + customer_user.full_name()

        if customer_user.username is not None:
            user_data += '<br>Pseudonym: ' + customer_user.username
        else:
            user_data += '<br> Sie haben kein Pseudonym vergeben'

        user_data += '<br>E-Mail Adresse: ' + customer_user.email + '<br>Paypal-Adresse: ' + customer_user.paypal +  '<br>Wohnort: ' + customer_user.location

        if(accepted == True):
            subject = 'Antrag auf Datenänderung akzeptiert'
            emailMsg = 'Ihr Antrag auf Datenänderung wurde akzeptiert.'
            msg = 'Ihr Antrag auf Datenänderung wurde akzeptiert und aktualisiert. Folgende Daten wurden aktualisiert: ' + user_data
        else:
            subject = 'Antrag auf Datenänderung abgelehnt'
            emailMsg = 'Ihr Antrag auf Datenänderung wurde abgelehnt.'
            msg = 'Ihr Antrag auf Datenänderung wurde leider abgelehnt. Folgende Daten sind weiterhin gespeichert: ' + user_data

        new_notification = Notification(
            sender_user=admin_user,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.CHANGE_PROFILE_CUSTOMER,
            receiver_user=customer_user)
        new_notification.save()
        NotificationEmailThread(new_notification.receiver_user, new_notification.subject, emailMsg).start()


    @staticmethod
    def request_remove_userprofile_administrator(customer_user_id):
        '''Diese Methode erstellt eine Notification wenn ein Kunde einen Antrag auf loeschung seiner Daten erstellt hat
        Diese Notification geht an alle Benutzer welche den Flag is_staff innehaben
        '''
        admins = User.objects.filter(is_staff = True)
        customer_user = get_object_or_404(User, id=customer_user_id)

        for admin in admins:
            subject = 'Antrag auf Löschung'
            msg = 'Der Kunde ' + customer_user.pseudonym_or_full_name() + ' hat einen Antrag auf Löschung gestellt.'
            new_notification = Notification(
                sender_user=customer_user,
                subject=subject,
                message=msg,
                received_date=datetime.now(),
                notification_type=Notification.REMOVE_PROFILE_ADMIN,
                receiver_user=admin)
        new_notification.save()
        NotificationEmailThread(new_notification.receiver_user, new_notification.subject, 'Nutzer möchte Account gelöscht haben.').start()


    @staticmethod
    def bann_unbann_user(admin_user_id, customer_user_id, is_banned):
        '''Diese Methode erstellt eine Notification wenn ein Benutzer gesperrt/entsperrt wurde'''
        admin = get_object_or_404(User, id=admin_user_id)
        customer_user = get_object_or_404(User, id=customer_user_id)

        if is_banned:
           subject = 'Sperrung des Accounts'
           msg = 'Ihr Account wurde gesperrt!'
        else:
           subject = 'Entsperrung des Accounts'
           msg = 'Ihr Account wurde entsperrt!'

        new_notification = Notification(
            sender_user=admin,
            subject=subject,
            message=msg,
            received_date=datetime.now(),
            notification_type=Notification.BANN_UNBANN_USER,
            receiver_user=customer_user)
        new_notification.save()
        NotificationEmailThread(new_notification.receiver_user, new_notification.subject, new_notification.message).start()

class NotificationEmailThread(threading.Thread):
    def __init__(self, recipient, subject=None, emailMessage=None):
        self.subject = 'book²: ' + (subject or 'Neue Benachrichtigung eingegangen')

        self.emailMessage = 'Hallo '+ recipient.first_name + ' '+ recipient.last_name +',<br><br>'
        if emailMessage:
            self.emailMessage += emailMessage
        else:
            self.emailMessage += 'Es liegt eine neue Benachrichtigung vor.'
        notificationsLink = settings.ENDPOINT + reverse('app_notification:notificationsPage')
        self.emailMessage += '<br><br><a href="'+notificationsLink+'">Zu den Nachrichten von book²</a>'
        self.emailMessage += '<br><br>Ihr Book²-Team'

        self.recipient = recipient
        self.address = self.recipient.email
        threading.Thread.__init__(self)

    def run (self):
        if(self.recipient.enabled_notifications_via_email):
            send_mail(self.subject, self.emailMessage, settings.EMAIL_HOST_USER,
                      [self.address], fail_silently=True, html_message=self.emailMessage)
