# -*- coding: utf-8 -*-
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.test import Client

from app_book.views import *
from app_user.models import *


class BookTest(TestCase):
    def setUp(self):
        self.user_username = 'test@test.test'
        self.user_password = 'supersavepassword'
        self.user_other_username = 'other@test.test'
        self.user_other_password = 'supersavepassword'

        self.error_message = 'Dies ist nicht Ihr Buch!'

        self.book_data = {
            'name': 'BookName',
            'author': 'authorName',
            'language': 'Language',
            'releaseDate': '19.11.2016',
            'pageNumber': '13',
            'isbn10': '1-78528-753-2',
            'isbn13': '978-1-78528-753-4',
            'description': 'description',
        }
        self.offer_data = {
            'price': '3.50',
            'shipping_price': '13.37',
            'active': 'on',
        }
        self.book_offer_data = self.book_data.copy()
        self.book_offer_data.update(self.offer_data)

        self.client = Client()

        User.objects.create_user(self.user_username, self.user_password)
        User.objects.create_user(self.user_other_username, self.user_other_password)

    def login_user(self):
        status = self.client.login(username=self.user_username, password=self.user_password)
        if status is False:
            raise Exception("Login error")

    def login_other_user(self):
        status = self.client.login(username=self.user_other_username, password=self.user_other_password)
        if status is False:
            raise Exception("Login error")

    def create_book(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        self.login_user()
        data = self.book_data.copy()
        with open('fixtures/image1.jpg', 'rb') as img:
            image = SimpleUploadedFile(img.name, img.read(), content_type='image/jpeg')
        data['image'] = image
        self.client.post(reverse('app_book:createBook'), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 0, offer)

    def create_book_offer(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        self.login_user()
        data = self.book_offer_data.copy()
        with open('fixtures/image1.jpg', 'rb') as img:
            image = SimpleUploadedFile(img.name, img.read(), content_type='image/jpeg')
        data['image'] = image
        self.client.post(reverse('app_book:createBook'), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)

    def check_permission_error(self, response):
        self.assertRedirects(response, reverse('app_book:books'))
        message = list(response.context['messages'])[1]
        self.assertTrue(self.error_message, message.message)

    def test_delete_unowned_book(self):
        self.create_book()
        book = Book.objects.all()

        self.login_other_user()
        response = self.client.delete(reverse('app_book:deleteBook', kwargs={'id': book.first().id}), follow=True)
        self.check_permission_error(response)

        book = Book.objects.all()
        self.assertEqual(len(book), 1, book)

    def test_publish_unowned_book(self):
        self.create_book()
        book = Book.objects.all()
        data = self.book_offer_data.copy()

        self.login_other_user()
        response = self.client.post(reverse('app_book:publishBook', kwargs={'id': book.first().id}), data=data, follow=True)
        self.check_permission_error(response)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 0, offer)

    def test_unpublish_unowned_book(self):
        self.create_book_offer()
        book = Book.objects.all()

        self.login_other_user()
        response = self.client.put(reverse('app_book:unpublishBook', kwargs={'id': book.first().id}), follow=True)
        self.check_permission_error(response)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)
        self.assertEqual(offer[0].active, True, offer)

    def test_edit_unowned_book(self):
        self.create_book()
        book = Book.objects.all()
        data = self.book_data.copy()
        data['name'] = 'NewName'

        self.login_other_user()
        response = self.client.put(reverse('app_book:editBook', kwargs={'id' : book.first().id}), data=data, follow=True)
        self.check_permission_error(response)

        book = Book.objects.all()
        self.assertEqual(book[0].name, self.book_data['name'])
        self.assertNotEqual(book[0].name, data['name'])

    def test_archive_contains_unowned_book(self):
        self.create_book()

        self.login_other_user()
        response = self.client.get(reverse('app_book:archivesPage'))

        self.assertNotContains(response, self.book_data['name'])

    def test_other_showcase_shows_unpublished(self):
        self.create_book_offer()

        book = Book.objects.all()
        self.client.put(reverse('app_book:unpublishBook', kwargs={'id': book.first().id}))
        offer = Offer.objects.all()
        self.assertEqual(len(offer), 1)
        self.assertEqual(offer[0].active, False)

        users = User.objects.all()
        self.login_other_user()
        response = self.client.get(reverse('app_book:showcase', kwargs={'user_id' : users.first().id}))

        self.assertNotContains(response, self.book_data['name'])

    def test_search_shows_unpublished(self):
        self.create_book_offer()

        book = Book.objects.all()
        self.client.put(reverse('app_book:unpublishBook', kwargs={'id': book.first().id}))
        offer = Offer.objects.all()
        self.assertEqual(len(offer), 1)
        self.assertEqual(offer[0].active, False)

        url = '/books?search_string='
        name = self.book_data['name'][:-2]
        self.login_other_user()
        response = self.client.get(url+name)

        self.assertNotContains(response, self.book_data['name'])