from app_book.models import Book
from .models import Payment
from app_book.services import unpublish_book
from paypal.standard.models import *

def complete_payment(payment):
    # remove book payment status
    payment.payment_status = ST_PP_COMPLETED
    payment.save()

    # move book to buyer
    book = payment.book
    book.user = payment.buyer_user
    book.save()
    offer = book.offer()
    offer.seller_user = payment.buyer_user
    offer.save()

    # remove book from showcase
    unpublish_book(book)

    # TODO notify seller
    # TODO notify buyer

def abort_payment(payment):
    # remove book payment status
    payment.payment_status = ST_PP_CANCELLED
    payment.save()

    # TODO notify seller
    # TODO notify buyer

def update_payment_from_paypal_ipn(payment, paypal_ipn):
    payment.payment_status = paypal_ipn.payment_status
    payment.last_ipn = paypal_ipn
    if payment.payment_status == ST_PP_COMPLETED:
        complete_payment(payment)
    elif payment.payment_status == ST_PP_CANCELLED:
        cancel_payment(payment)
    payment.save()
