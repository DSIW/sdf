# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from django.test import Client

from app_book.views import *
from app_user.models import *


class BookTest(TestCase):
    def setUp(self):
        user_username = 'test@fixture_mail.com'
        user_password = 'supersavepassword'

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

        User.objects.create_user(user_username, user_password)
        status = self.client.login(username=user_username, password=user_password)
        if status is False:
            raise Exception("Login error")

    def test_create_book(self):
        book = Book.objects.all()
        self.assertEqual(len(book), 0)

        self.client.post(reverse('app_book:createBook'), data=self.book_data)

        book = Book.objects.all()
        self.assertEqual(len(book), 1)

    def test_create_book_with_Offer(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        self.client.post(reverse('app_book:createBook'), data=self.book_offer_data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)

    def test_handle_edit_book_empty_field(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        data = self.book_offer_data.copy()

        for attrib in data.keys():
            # skip fields that can be blank
            if attrib in Book._meta._forward_fields_map.keys() and Book._meta._forward_fields_map[attrib].blank:
                continue
            if attrib in Offer._meta._forward_fields_map.keys() and Offer._meta._forward_fields_map[attrib].blank:
                continue

            # restore data state
            data = self.book_offer_data.copy()
            data[attrib] = ''

            self.client.post(reverse('app_book:createBook'), data=data)

            book = Book.objects.all()
            offer = Offer.objects.all()

            self.assertEqual(len(book), 0, attrib)
            self.assertEqual(len(offer), 0, attrib)

    def test_handle_edit_book_missing_field(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        data = self.book_offer_data.copy()

        for attrib in data.keys():
            # skip fields that can be blank
            if attrib in Book._meta._forward_fields_map.keys() and Book._meta._forward_fields_map[attrib].blank:
                continue
            if attrib in Offer._meta._forward_fields_map.keys() and Offer._meta._forward_fields_map[attrib].blank:
                continue

            # restore data state
            data = self.book_offer_data.copy()
            del data[attrib]

            self.client.post(reverse('app_book:createBook'), data=data)

            book = Book.objects.all()
            offer = Offer.objects.all()

            self.assertEqual(len(book), 0, attrib)
            self.assertEqual(len(offer), 0, attrib)

    def test_handle_edit_book_active_false(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        data = self.book_offer_data.copy()
        data['active'] = 'off'

        self.client.post(reverse('app_book:createBook'), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 0, offer)

    def test_handle_edit_book_atomic_transaction_bad_offer(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        data = self.book_offer_data.copy()
        data['active'] = 'on'
        data['price'] = 'bogusVal'

        self.client.post(reverse('app_book:createBook'), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0, book)
        self.assertEqual(len(offer), 0, offer)

    def test_handle_edit_book_atomic_transaction_bad_book(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        data = self.book_offer_data.copy()
        del data['name']

        self.client.post(reverse('app_book:createBook'), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0, book)
        self.assertEqual(len(offer), 0, offer)

    def test_handle_edit_book_unpublish(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        data = self.book_offer_data.copy()
        self.client.post(reverse('app_book:createBook'), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)

        data = self.book_offer_data.copy()
        data['active'] = 'off'
        self.client.post(reverse('app_book:editBook', kwargs={'id': book.first().id}), data=data)
        offer = Offer.objects.all()

        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)
        self.assertEqual(offer[0].active, False, offer)

    def test_delete_book(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        data = self.book_offer_data.copy()
        self.client.post(reverse('app_book:createBook'), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)

        self.client.delete(reverse('app_book:deleteBook', kwargs={'id': book.first().id}), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0, book)
        self.assertEqual(len(offer), 0, offer)

    def test_publish_book(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        self.client.post(reverse('app_book:createBook'), data=self.book_data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 0, offer)

        data = data = self.book_offer_data.copy()
        self.client.post(reverse('app_book:publishBook', kwargs={'id': book.first().id}), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)

    def test_unpublish_book(self):
        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 0)
        self.assertEqual(len(offer), 0)

        data = data = self.book_offer_data.copy()
        self.client.post(reverse('app_book:createBook'), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)

        self.client.put(reverse('app_book:unpublishBook', kwargs={'id': book.first().id}), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)
        self.assertEqual(offer[0].active, False, offer)
