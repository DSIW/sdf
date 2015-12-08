# -*- coding: utf-8 -*-
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, RequestFactory
from app_user.forms import RegistrationForm
from app_user.models import User


class FormTests(TestCase):

    def setUp(self):
        #pwd = test
        User.objects.create(first_name="Bernd", last_name="Lauert", username="testuser_fix", password="pbkdf2_sha256$20000$d8Zk6o89XrYZ$O9WiWbzttZu4TGpZn2ZZf5UJ5cwhJq2c/ZtrRbUWQ/0=")
        self.form_data = {
            'username': 'testuser',
            'first_name': 'Bernd',
            'last_name': 'Lullert',
            'email': 'test@mail.com',
            'paypal': 'test@mail.com',
            'password1': 'test',
            'password2': 'test',
        }
        self.rq = RequestFactory()

    def test_validRegistrationWithAcceptableProfileImage(self):
        data = self.form_data.copy()
        with open('fixtures/image1.jpg', 'rb') as img:
            data['file'] = SimpleUploadedFile(img.name, img.read())
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_registerAlreadyTakenNickname(self):
        data = self.form_data.copy()
        data['username'] = 'testuser_fix'
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_validRegistrationWithUnacceptableProfileImage(self):
        #TODO implement image validation
        None

    def test_invalidMailAddress(self):
        data = self.form_data.copy()
        data['email'] = 'test'
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_notMatchingPasswords(self):
        data = self.form_data.copy()
        data['password1'] = 'test1'
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
    def test_registerWithEmptyUsername(self):
        data = self.form_data.copy()
        data['username'] = None
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())