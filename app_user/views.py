# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from braces.views import FormMessagesMixin
from smtplib import SMTPRecipientsRefused
from .models import User, ConfirmEmail
from .forms import CustomUpdateForm,RegistrationForm

# Custom Current User Decorator

def current_user(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs.get("pk")
        if id != str(request.user.pk) and not request.user.is_superuser:
            messages.add_message(request, messages.ERROR, 'Dies ist nicht Ihr Account!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return func(request, *args, **kwargs)
    return check_and_call

def register_user(request):
    if request.method == 'POST':
        try:
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.profileImage = request.FILES.get('profileImage')
                user = form.save()
                form.sendConfirmEmail(request, user)

                messages.add_message(request, messages.SUCCESS, 'Sie haben sich erfolgreich registriert.')
                return HttpResponseRedirect(reverse('app:startPage'))
        except SMTPRecipientsRefused:
            messages.add_message(request, messages.ERROR, 'Es konnte keine Validierungsemail zur eingegebenen E-Mail Adresse ' + user.email + ' verschickt werden')
            render_to_response('app_user/register.html', {'form': form}, RequestContext(request))

    else:
        form = RegistrationForm()
    return render_to_response('app_user/register.html', {'form': form}, RequestContext(request))

class UserUpdate(FormMessagesMixin, UpdateView):
    model = User
    model._meta.get_field('username').error_messages = {'unique': 'Das gewählte Pseudonym ist bereits vergeben.',
                                                        'invalid': 'Bitte ein gültiges Pseudonym eingeben. Dieses darf nur Buchstaben, Ziffern und @/./+/-/_ enthalten.'}
    form_class = CustomUpdateForm
    form_invalid_message = _('Account konnte nicht aktualisiert werden.')
    form_valid_message = _('Account wurde erfolgreich aktualisiert.')
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('app:startPage')

    @method_decorator(current_user)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdate, self).dispatch(*args, **kwargs)

def confirm_email(request, uuid):
    confirmEmail = ConfirmEmail.objects.filter(uuid=uuid).first()
    if confirmEmail is not None:
        user = confirmEmail.user
        if user.emailConfirm:
            messages.add_message(request, messages.INFO, 'Ihre E-Mail Adresse ' + user.email + ' ist bereits bestätigt')
        else:
            user.emailConfirm = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Ihre E-Mail Adresse ' + user.email + ' wurde erfolgreich bestätigt')
    else:
        messages.add_message(request, messages.ERROR, 'Ihre E-Mail Adresse konnte nicht bestätigt werden')
    return HttpResponseRedirect(reverse('app:startPage'))


def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.add_message(request, messages.SUCCESS, 'Das Passwort wurde erfolgreich geändert')
            return HttpResponseRedirect(reverse('app:startPage'))
    else:
        form = PasswordChangeForm(user=request.user)
    return render_to_response('app/change_password.html', {'form': form}, RequestContext(request))
