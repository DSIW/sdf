from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from .models import Book
from .models import Counteroffer


def can_show_book(func):
    def check_and_call(request, *args, **kwargs):
        kwargs_id = kwargs.get("id")
        if kwargs_id is None:
            return func(request, *args, **kwargs)
        book = get_object_or_404(Book, id=kwargs_id)
        if book.is_private() and not book.user.id == request.user.id:
            messages.add_message(request, messages.ERROR, 'Sie haben keine Berechtigung das Buch anzusehen!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/books'))
        return func(request, *args, **kwargs)
    return check_and_call


def can_change_book(func):
    def check_and_call(request, *args, **kwargs):
        kwargs_id = kwargs.get("id")
        if kwargs_id is None:
            return func(request, *args, **kwargs)
        book = get_object_or_404(Book, id=kwargs_id)
        if not book.user.id == request.user.id:
            messages.add_message(request, messages.ERROR, 'Sie haben keine Berechtigung das Buch zu bearbeiten!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/books/' + str(book.id) + "/"))
        return func(request, *args, **kwargs)
    return check_and_call


def can_reply_to_offer(func):
    def check_and_call(request, *args, **kwargs):
        kwargs_id = kwargs.get("id")
        if id is None:
            return func(request, *args, **kwargs)
        counteroffer = get_object_or_404(Counteroffer, id=kwargs_id)
        offer = counteroffer.offer
        if not offer.seller_user.id == request.user.id:
            messages.add_message(request, messages.ERROR, 'Sie haben keine Berechtigung auf das Gegenangebot zu antworten!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/books/' + str(offer.book.id) + "/"))
        if not counteroffer.active:
            messages.add_message(request, messages.ERROR, 'Das Gegenangebot ist nicht mehr aktiv!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/notifications/'))
        return func(request, *args, **kwargs)
    return check_and_call
