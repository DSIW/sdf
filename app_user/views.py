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
from .models import User, ConfirmEmail

from .forms import RegistrationForm


# Create your views here.

# Custom Current User Decorator
def current_user(func):
    def check_and_call(request, *args, **kwargs):
        id = kwargs["pk"]
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        if not (id == str(request.user.pk)):
            messages.add_message(request, messages.ERROR, 'Dies ist nicht Ihr Account!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return func(request, *args, **kwargs)
    return check_and_call

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.sendConfirmEmail(request, user)

            messages.add_message(request, messages.SUCCESS, 'Sie haben sich erfolgreich registriert.')
            return HttpResponseRedirect(reverse('app:startPage'))
    else:
        form = RegistrationForm()
    return render_to_response('app_user/register.html', {'form': form}, RequestContext(request))

class UserUpdate(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'paypal']
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
