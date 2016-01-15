from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from .models import Book

def can_show_book(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs.get("id")
        if id == None:
            return func(request, *args, **kwargs)
        book = get_object_or_404(Book, id=id)
        if book.is_private() and not (book.user.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Sie haben keine Berechtigung das Buch anzusehen!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return func(request, *args, **kwargs)
    return check_and_call


def can_change_book(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs.get("id")
        if id == None:
            return func(request, *args, **kwargs)
        book = get_object_or_404(Book, id=id)
        if not (book.user.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Sie haben keine Berechtigung das Buch zu bearbeiten!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return func(request, *args, **kwargs)
    return check_and_call