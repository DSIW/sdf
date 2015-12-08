from app_book.models import Book
from app_notification.models import Notification
from .models import Payment
from app_book.services import unpublish_book
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
            offer.delete()
            book.save()
    except ValueError as e:
        return False

    # TODO: handle counter offers
    return True

def complete_payment(payment):
    # remove book payment status
    payment.payment_status = ST_PP_COMPLETED
    payment.save()

    # move book to buyer
    book = payment.book
    change_ownership(book.id, payment.buyer_user.id)

    # notify seller
    Notification.fastbuy(payment.buyer_user, payment.seller_user, payment.book)


def abort_payment(payment):
    # remove book payment status
    payment.payment_status = ST_PP_CANCELLED
    payment.save()


def update_payment_from_paypal_ipn(payment, paypal_ipn):
    payment.payment_status = paypal_ipn.payment_status
    payment.last_ipn = paypal_ipn
    if payment.payment_status == ST_PP_COMPLETED:
        complete_payment(payment)
    elif payment.payment_status == ST_PP_CANCELLED:
        cancel_payment(payment)
    payment.save()