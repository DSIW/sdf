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
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import get_object_or_404

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as loginview
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.core.mail import EmailMessage
from .models import User, ConfirmEmail, PasswordReset, ChangeUserData
from app_notification.models import Notification

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from braces.views import FormMessagesMixin
from smtplib import SMTPRecipientsRefused
from .decorators import can_change_user
from .models import User, ConfirmEmail
from app_book.models import Book, Offer
from .forms import CustomUpdateForm,RegistrationForm, UsernameForm, ImageForm
from app_payment.models import SellerRating


# Custom Current User Decorator
from django.conf import settings

def login_user(request):
    # prevent a logged in user from accessing the login page
    if(request.user.pk):
        return HttpResponseRedirect(reverse('app_book:archivesPage'))

    form = AuthenticationForm
    if request.method == "POST":

        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                if User.objects.filter(pk=user.id).first().emailConfirm == 1:
                    login(request, user)
                    # Redirect to a success page.
                elif settings.DEBUG:
                    messages.add_message(request, messages.INFO, format_html("Die E-Mail-Adresse wurde noch nicht bestätigt. Debugmodus aktiv, Login gestattet. <a href='{}'>Aktivierungslink erneut zusenden</a>", reverse('app_user:resend_confirmation_mail', kwargs={'email': email})))
                    login(request, user)
                else:
                    messages.add_message(request, messages.ERROR, format_html("Die E-Mail-Adresse wurde noch nicht bestätigt. <a href='{}'>Aktivierungslink erneut zusenden</a>", reverse('app_user:resend_confirmation_mail', kwargs={'email': email})))
            else:
                # Return a 'disabled account' error message
                messages.add_message(request, messages.ERROR, 'Das Benutzerkonto ist deaktiviert.')
            return HttpResponseRedirect(request.POST['next'] or reverse('app_book:archivesPage'))
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request, messages.ERROR, 'Loginversuch fehlgeschlagen.')
            return render_to_response('registration/login.html', {'form': form}, RequestContext(request))
    else:
        return render_to_response('registration/login.html', {'form': form, 'next': request.GET.get('next') or ''}, RequestContext(request))


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
        user = User.objects.filter(email=email).first()
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
    # prevent a logged in user from accessing the registration page
    if(request.user.pk):
        return HttpResponseRedirect(reverse('app_book:archivesPage'))

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.profileImage = request.FILES.get('profileImage')
            user = form.save()
            form.sendConfirmEmail(request, user)
            messages.add_message(request, messages.SUCCESS, 'Sie haben sich erfolgreich registriert.')
            return HttpResponseRedirect(reverse('app_user:login'))
    else:
        form = RegistrationForm()
    return render_to_response('app_user/register.html', {'form': form}, RequestContext(request))

@login_required
@can_change_user
def user_update(request, pk):
    user = User.objects.filter(id=pk).first()
    data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'location': user.location,
            'paypal' : user.paypal
        }

    changeUserDataTmp = ChangeUserData.objects.filter(user_id=user.id).first()
    if changeUserDataTmp is not None:
        if request.method == "DELETE":
            changeUserDataTmp.delete()
            messages.add_message(request, messages.SUCCESS, "Ihr Antrag wurde gelöscht")
            return HttpResponseRedirect(reverse('app_user:edit_profile', kwargs={'pk':request.user.id}))
        else:
            return render_to_response('app_user/user_update_error.html',{}, RequestContext(request))

    if request.method == "POST":
        form = CustomUpdateForm(request.POST, initial=data)

        if not form.has_changed():
            messages.add_message(request, messages.ERROR,
                     "Es wurde keine Daten geändert")
            return render_to_response('app_user/user_update_form.html', {'form': form}, RequestContext(request))
        if form.is_valid():
            form.user = user
            if form.cleaned_data["delete_account"]:
                user.is_active = False;
                user.showcaseDisabled = True;
                user.save();
                Notification.request_remove_userprofile_administrator(user.id)
                messages.add_message(request, messages.SUCCESS,
                     "Ihr Antrag wurde erfolgreich versendet und wird in Kürze von einem Moderator bearbeitet. Ihr Profil ist ab sofort deaktiviert und wird nach der Bestätigung des Admins gelöscht")
                return HttpResponseRedirect(reverse('app_user:logout')+'?next=/')

            else:
                changeUserData = form.save(commit=False)
                changeUserData.user_id = user.id
                changeUserData.save()
                Notification.request_change_userprofile_administrator(user.id, changeUserData)
                messages.add_message(request, messages.SUCCESS,
                         "Ihr Antrag wurde erfolgreich versendet und wird in Kürze von einem Moderator bearbeitet. Sie erhalten anschließend eine Benachrichtigung")
                return HttpResponseRedirect(reverse('app_user:user-details', kwargs={'pk':request.user.id}))
    else:
        form = CustomUpdateForm(data, initial=data)
    return render_to_response('app_user/user_update_form.html', {'form': form}, RequestContext(request))

def user_details(request, pk):
    template_name = 'app_user/detail.html'
    user = User.objects.filter(id=pk).first()
    user.books_count = len(user.offer_set.exclude(active = False))

    autoopen = {
        'usernamemodal': 'false',
        'imagemodal' : 'false'
    }

    if request.method == "POST" and request.POST.get("form") == "updateProfileImage":
        form = UsernameForm()
        imageform = ImageForm(request.POST, request.FILES)
        if imageform.is_valid():
            newImage = request.FILES.get('profileImage')
            if request.user.id == user.id:
                if newImage is not None:
                    user.profileImage = newImage
                    user.save()
                elif ('delete_saved_image' in request.POST and request.POST['delete_saved_image'] == 'on'):
                    user.profileImage = None
                    user.save()
            return HttpResponseRedirect(reverse('app_user:user-details', kwargs={'pk':request.user.id}))
        else:
            autoopen["imagemodal"] = 'true'
    elif request.method == "POST" and request.POST.get("form") == "updateUsername" and user.id == request.user.id:
        form = UsernameForm(request.POST)
        imageform = ImageForm()
        if form.is_valid():
            user.username = form.clean_username()
            user.save()
        else:
            autoopen["usernamemodal"] = 'true'
    else:
        form = UsernameForm()
        imageform = ImageForm(instance=user)


    return render_to_response(template_name, {'user': user, 'form': form, 'imageform' : imageform, 'autoopen': autoopen}, RequestContext(request))

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
    return HttpResponseRedirect(reverse('app_user:login'))

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.add_message(request, messages.SUCCESS, 'Das Passwort wurde erfolgreich geändert')
            return HttpResponseRedirect(reverse('app_user:user-details', kwargs={'pk':request.user.id}))
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

        link = 'https://' + HttpRequest.get_host(request) + reverse('app_user:new_password', kwargs={'uuid': confirmId})
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

def user_ratings(request, id):
    user = User.objects.filter(pk=id).first()
    ratings = SellerRating.objects.filter(rated_user_id=id)
    return render_to_response('app_user/user_ratings.html',{'rated_user':user,'ratings':ratings},RequestContext(request))

def change_user_profile(request, change_user_data_id, accepted):
    change_user_data = get_object_or_404(ChangeUserData, id=change_user_data_id)
    user = change_user_data.user

    if(accepted):
        user.first_name = change_user_data.first_name
        user.username = change_user_data.username
        user.last_name = change_user_data.last_name
        user.email = change_user_data.email
        user.location = change_user_data.location
        user.paypal = change_user_data.paypal

        user.save()

    change_user_data.delete()
    Notification.request_change_userprofile_customer(request.user.id, user.id, accepted)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def change_user_profile_decline(request, change_user_data_id):
    change_user_profile(request, change_user_data_id, False)
    messages.add_message(request, messages.SUCCESS, 'Antrag auf Benutzerdatenänderung wurde erfolgreich abgelehnt')
    return HttpResponseRedirect(reverse('app_notification:notificationsPage'))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def change_user_profile_accept(request, change_user_data_id):
    change_user_profile(request, change_user_data_id, True)
    messages.add_message(request, messages.SUCCESS, 'Benutzerdaten wurden erfolgreich aktualisiert')
    return HttpResponseRedirect(reverse('app_notification:notificationsPage'))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def remove_user(request, remove_user_id):

    '''Loesche Buecher'''
    books = Book.objects.filter(user_id = remove_user_id)
    for book in books:
        book.delete()

    '''Loesche Schaufenster'''
    offers = Offer.objects.filter(seller_user_id = remove_user_id)
    for offer in offers:
        offer.delete()


    user = get_object_or_404(User, id=remove_user_id)
    user.delete()


    messages.add_message(request, messages.SUCCESS, 'Benutzer und alle seine Aktvitäten wurden erfolgreich gelöscht')
    return HttpResponseRedirect(reverse('app_notification:notificationsPage'))

# Call via AJAX
@login_required
def toggleStaff(request, pk):
    if request.method == 'POST' and request.user.is_superuser:
        user = User.objects.filter(id=pk).first()
        is_staff = user.is_staff
        user.is_staff = not is_staff
        user.save()
        return JsonResponse({'state': not is_staff})
    return JsonResponse({'error': True})
