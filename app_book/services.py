from app_book.models import Counteroffer
from app_notification.models import Notification


def unpublish_book(book):
    offer = book.offer()
    if offer is not None:
        offer.active = False
        offer.save()

def decline_all_counteroffers_for_offer(offer):
    counteroffers = Counteroffer.objects.filter(offer=offer, active=True, accepted=False)
    for co in counteroffers:
        co.decline()
        Notification.counteroffer_decline(co, co.creator, offer.book)
