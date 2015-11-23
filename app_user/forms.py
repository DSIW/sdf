# -*- coding: utf-8 -*-

import threading
from django import forms
from django.http import HttpRequest
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm

from .models import User, ConfirmEmail
from app.widgets import CustomFileInput

class RegistrationForm(UserCreationForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()

    paypal = forms.EmailInput()
    email = forms.EmailInput()
    profileImage = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['username'].required = False
        self.fields['password2'].help_text = None
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['profileImage'].required = False
        self.fields['profileImage'].widget = CustomFileInput()


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'paypal', 'password1', 'password2', 'profileImage']

        def clean_username(self):
            return self.cleaned_data['username'] or None


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.paypal = self.cleaned_data['paypal']
        user.profileImage = self.cleaned_data['profileImage']
        user.username = self.cleaned_data['username'] or None

        if commit:
            user.save()

        return user

    def sendConfirmEmail(self, request, user):
        confirmEmail = ConfirmEmail.objects.filter(user=user).first()
        if confirmEmail is None:
            confirmId = get_random_string(length=32)
            user = User.objects.filter(email=request.POST.get('email')).first()
            confirmEmail = ConfirmEmail()
            confirmEmail.uuid = confirmId
            confirmEmail.user = user
            confirmEmail.save()
        link = 'http://' + HttpRequest.get_host(request) + reverse('app_user:confirm_email', kwargs={'uuid': confirmEmail.uuid})
        emailMessage = 'Hallo '+ request.POST.get('first_name') + ' '+request.POST.get('last_name') +', <br><br>vielen dank für die Registrierung in book².<br> Zur Bestätigung Ihrer E-Mail Adresse betätigen Sie bitte folgenden Link: <a href="' + link + '">Bestätigen</a><br>Sollten Sie den Link nicht nutzen könnten dann kopieren Sie bitte folgende URL in Ihren Browser:<br> ' + link + '<br><br>Wir wünschen Ihnen viel Spaß beim Shoppen<br>Ihr book² team'
        EmailThread('Registrierungsbestätigung book²', emailMessage, request).start()


class EmailThread(threading.Thread):
    def __init__(self, subject, emailMessage, request):
        self.subject = subject
        self.emailMessage = emailMessage
        self.request = request
        threading.Thread.__init__(self)

    def run (self):
        send_mail(self.subject, self.emailMessage, settings.EMAIL_HOST_USER,
                  [self.request.POST.get('email')], fail_silently=True, html_message=self.emailMessage)

class CustomUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomUpdateForm, self).__init__(*args, **kwargs)

        self.fields['profileImage'].required = False
        self.fields['profileImage'].widget = CustomFileInput()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'paypal', 'profileImage']

    def clean_username(self):
        return self.cleaned_data['username'] or None
