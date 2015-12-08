# -*- coding: utf-8 -*-
import re
from django.contrib import messages
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import SimpleCookie
from django.test import TestCase
from app_user.models import User, ConfirmEmail
from django.test.utils import setup_test_environment

class ViewTests(TestCase):

    def setUp(self):
        #pwd = test
        user = User.objects.create(first_name="Bernd", last_name="Lauert", username="testuser_fix", password="pbkdf2_sha256$20000$d8Zk6o89XrYZ$O9WiWbzttZu4TGpZn2ZZf5UJ5cwhJq2c/ZtrRbUWQ/0=")
        ConfirmEmail.objects.create(uuid="mfYtKJSl6Y0cPNr8Wa5f0mdY130KseKw", user=user)
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Bernd',
            'last_name': 'Lullert',
            'email': 'test@mail.com',
            'paypal': 'test@mail.com',
            'password1': 'test',
            'password2': 'test',
        }
        self.confirmation_uuid = 'mfYtKJSl6Y0cPNr8Wa5f0mdY130KseKw'
        setup_test_environment()

    def test_register_user_valid(self):
        user = User.objects.all()
        self.assertEqual(len(user), 1)

        response = self.client.post(reverse('app_user:register'), data=self.user_data)
        self.assertEqual(response.status_code, 302)

        user = User.objects.all()
        self.assertEqual(len(user), 2)

    def test_register_user_invalid_mail(self):
        user = User.objects.all()
        self.assertEqual(len(user), 1)
        data = self.user_data.copy()
        data['email'] = 'a'
        response = self.client.post(reverse('app_user:register'), data=data)
        self.assertEqual(response.status_code, 200)

        user = User.objects.all()
        self.assertEqual(len(user), 1)

    def test_confirm_mail_valid(self):
        user = User.objects.all().first()
        confirmMail = ConfirmEmail.objects.all().filter(user=user.user_ptr).first()
        self.assertEqual(self.confirmation_uuid, confirmMail.uuid)
        data = {'email': 'dummy'}

        response = self.client.post(reverse('app_user:confirm_email', kwargs={'uuid': confirmMail.uuid}), data=data)

        self.assertRedirects(response, reverse('app:startPage'))
        #25 = SUCCESS
        self.assertNotEqual(re.match(".*,0,25,", response.cookies['messages'].value), None)
        user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.emailConfirm, True)

    def test_invalid_confirmation(self):
        data = {'email': 'dummy'}
        response = self.client.post(reverse('app_user:confirm_email', kwargs={'uuid': 'wrong'}), data=data)

        self.assertRedirects(response, reverse('app:startPage'))
        #40 = ERROR
        self.assertNotEqual(re.match(".*,0,40,", response.cookies['messages'].value), None)
        self.assertEqual(response.status_code, 302)





