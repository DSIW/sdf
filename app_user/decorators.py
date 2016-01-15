from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from .models import User

def can_change_user(func):
    def check_and_call(request, *args, **kwargs):
        kwargs_pk = kwargs.get("pk")
        if kwargs_pk is None:
            return func(request, *args, **kwargs)
        if not (int(kwargs_pk) == request.user.id):
            messages.add_message(request, messages.ERROR, 'Sie haben keine Berechtigung den Benutzer zu bearbeiten!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/accounts/' + str(request.user.id)))
        return func(request, *args, **kwargs)
    return check_and_call