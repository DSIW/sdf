from django.core.exceptions import ObjectDoesNotExist

from app_book.models import Book
from app_notification.models import Notification
from .models import Payment
from app_book.services import unpublish_book, decline_all_counteroffers_for_offer
from paypal.standard.models import *
from django.db import transaction

@transaction.atomic
def change_ownership(book_id, to_user_id):
    if not isinstance(to_user_id, int) or to_user_id < 0 \
           or not isinstance(book_id, int) or book_id < 0:
        return False

    try:
        book = Book.objects.get(pk=book_id)
        offer = book.offer_set.first()
    except ObjectDoesNotExist as e:
        return False

    book.user_id = to_user_id

    try:
        with transaction.atomic():
            if offer:
                offer.delete()
            book.save()
    except ValueError as e:
        return False

    # TODO: handle counter offers
    return True

def complete_payment(payment):
    if payment.is_active() and not payment.is_completed():
        # remove book payment status
        payment.payment_status = ST_PP_COMPLETED
        payment.save()

        # move book to buyer
        book = payment.book
        change_ownership(book.id, payment.buyer_user.id)

        Notification.fastbuy(payment.buyer_user, payment.seller_user, payment.book)
        Notification.request_rating(payment)
        return True
    return False

def abort_payment(payment, notification = False):
    if payment.is_active() and not payment.is_cancelled():
        payment.payment_status = ST_PP_CANCELLED
        payment.save()
        if notification:
            Notification.abort_unpaid_payment(payment)
        return True
    return False

def update_payment_from_paypal_ipn(payment, paypal_ipn):
    payment.payment_status = paypal_ipn.payment_status
    payment.last_ipn = paypal_ipn
    if payment.payment_status == ST_PP_COMPLETED:
        complete_payment(payment)
    elif payment.payment_status == ST_PP_CANCELLED:
        abort_payment(payment)

def start_payment(payment, offer, buyer):
    if payment.id is None:
        payment.init_process(offer, buyer)
        decline_all_counteroffers_for_offer(offer)
        payment.save()
        return True
    return False
