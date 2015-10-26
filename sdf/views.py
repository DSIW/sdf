'''
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.forms import  AuthenticationForm

from django.core.context_processors import csrf
import logging

logger = logging.getLogger(__name__)


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("login.html", c)


def authetification(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            render_to_response("app/start.html", {"username": request.user.username})
    else:
        error_message = {'error_message': 'login failed'}
        render_to_response("login.html", error_message)


def logout(request):
    auth.logout(request)
    render_to_response("app/start.html")
'''