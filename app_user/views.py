# -*- coding: utf-8 -*-

from django.http import HttpRequest
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.views.generic.edit import UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.views import login as loginview

from django.core.mail import EmailMessage
from .models import User, ConfirmEmail, PasswordReset

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from braces.views import FormMessagesMixin
from smtplib import SMTPRecipientsRefused
from .models import User, ConfirmEmail
from .forms import CustomUpdateForm, RegistrationForm


# Custom Current User Decorator
from sdf import settings

def login_user(request):
    form = AuthenticationForm
    if request.method == "POST":

        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                if User.objects.get(pk=user.id).emailConfirm == 1:
                    login(request, user)
                    return HttpResponseRedirect(reverse('app:startPage'))
                    # Redirect to a success page.
                else:
                    messages.add_message(request, messages.ERROR, format_html("Die E-Mail-Adresse wurde noch nicht bestätigt. <a href='{}'>Aktivierungslink erneut zusenden</a>", reverse('app_user:resend_confirmation_mail', kwargs={'email': email})))
                    if settings.DEBUG:
                        messages.add_message(request, messages.INFO, format_html("Die E-Mail-Adresse wurde noch nicht bestätigt. Debugmodus aktiv, Login gestattet. <a href='{}'>Aktivierungslink erneut zusenden</a>", reverse('app_user:resend_confirmation_mail', kwargs={'email': email})))
                        login(request, user)
                    return HttpResponseRedirect(reverse('app:startPage'))
            else:
                # Return a 'disabled account' error message
                messages.add_message(request, messages.ERROR, 'Das Benutzerkonto ist deaktiviert.')
                return HttpResponseRedirect(reverse('app:startPage'))
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request, messages.ERROR, 'Loginversuch fehlgeschlagen.')
            return render_to_response('registration/login.html', {'form': form}, RequestContext(request))
    else:
        print("GET")
        return render_to_response('registration/login.html', {'form': form}, RequestContext(request))


def current_user(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs.get("pk")
        if id != str(request.user.pk) and not request.user.is_superuser:
            messages.add_message(request, messages.ERROR, 'Dies ist nicht Ihr Account!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return func(request, *args, **kwargs)

    return check_and_call


def resend_confirmation_mail(request, email):
    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user == None:
            messages.add_message(request, messages.ERROR, 'Diese E-Mail-Adresse ist nicht bekannt.')
            return HttpResponseRedirect(reverse('app:startPage'))
        if user.emailConfirm == 1:
            messages.add_message(request, messages.INFO, 'Ihre E-Mail Adresse ' + user.email + ' ist bereits bestätigt')
            return HttpResponseRedirect(reverse('app:startPage'))
        if user.emailConfirm == 0:
            messages.add_message(request, messages.INFO, 'Validierungsemail an '+ user.email +' verschickt.')
            form = RegistrationForm()
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['first_name'] = user.first_name
            request.POST['last_name'] = user.last_name
            request.POST['email'] = user.email
            request.POST._mutable = mutable
            form.sendConfirmEmail(request, user)
            return HttpResponseRedirect(reverse('app:startPage'))



def register_user(request):
    if request.method == 'POST':
        result = False
        try:
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.profileImage = request.FILES.get('profileImage')
                user = form.save()
                result = form.sendConfirmEmail(request, user)
        except SMTPRecipientsRefused:
            result = False
        if result:
            messages.add_message(request, messages.SUCCESS, 'Sie haben sich erfolgreich registriert.')
            return HttpResponseRedirect(reverse('app:startPage'))
        else:
            messages.add_message(request, messages.ERROR, 'Es konnte keine Validierungsemail zur eingegebenen E-Mail Adresse ' + request.POST.get('email') + ' verschickt werden')
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
            messages.add_message(request, messages.SUCCESS,
                                 'Ihre E-Mail Adresse ' + user.email + ' wurde erfolgreich bestätigt')
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
    action = reverse('app_user:change_password')
    return render_to_response('app_user/password.html', {'form': form, 'action': action}, RequestContext(request))

def sendPasswordResetEmail(request):
    email = request.POST.get('email', '')
    user=User.objects.filter(email=email).first()

    result = False

    if user is not None:
        subject = "Password Zurücksetzen book²"

        confirmId = get_random_string(length=32)
        entry = PasswordReset.objects.filter(user=user).first()

        # create entry if not exists
        if entry is None:
            entry = PasswordReset()

        # add/edit entry
        entry.uuid = confirmId
        entry.user = user
        entry.save()

        link = 'http://' + HttpRequest.get_host(request) + reverse('app_user:new_password', kwargs={'uuid': confirmId})
        message = 'Hallo '+ user.first_name + ' ' + user.last_name + ',<br><br> um Ihr Passwort zurückzusetzen, klicken Sie bitte auf den Link: <a href="' + link + '">Bestätigen</a><br>Sollten Sie den Link nicht nutzen könnten dann kopieren Sie bitte folgende URL in Ihren Browser:<br> ' + link + '<br><br>Ihr book² team'

        msg = EmailMessage(subject, message, [], [email])
        msg.content_subtype = "html"
        result = msg.send()

    return result

# Diese Methode setzt das Password zurück, in dem eine EMail an den Benutzer geschickt wird.
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            result = sendPasswordResetEmail(request)

            if result:
                messages.add_message(request, messages.SUCCESS, 'Es wurde eine Email versendet!')
            else:
                messages.add_message(request, messages.ERROR, 'Bitte überprüfen Sie, ob alle Felder korrekt sind. Zulässige Zeichen: a-z, 0-9, -, _ und @.')

            return HttpResponseRedirect(reverse('app:startPage'))
    else:
        form = PasswordResetForm()
    action = reverse('app_user:reset_password')
    return render_to_response('app_user/password.html', {'form': form, 'action': action}, RequestContext(request))

# Diese Methode setzt das Password eines Benutzers.
def password_new(request, uuid):
    entry = PasswordReset.objects.filter(uuid=uuid).first()

    if entry is None:
         messages.add_message(request, messages.ERROR, 'Ungültiger Vorgang!')
         return HttpResponseRedirect(reverse('app:startPage'))

    user=entry.user

    if request.method == 'POST':
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            entry.delete()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Das Passwort wurde erfolgreich geändert')
            return HttpResponseRedirect(reverse('app:startPage'))

    else:
        form = SetPasswordForm(user=user)
    action = reverse('app_user:new_password', kwargs={'uuid': uuid})
    return render_to_response('app_user/password.html', {'form': form, 'action': action}, RequestContext(request))
