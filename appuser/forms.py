# coding=utf-8
from django import forms

from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    first_name = forms.TextInput()
    last_name = forms.TextInput()

    paypal = forms.EmailInput()
    email = forms.EmailInput()

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name', 'last_name', 'email','paypal', 'password1', 'password1')


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.paypal = self.cleaned_data['paypal']

        if commit:
            user.save()
