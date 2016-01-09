# -*- coding: utf-8 -*-
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase, RequestFactory
from django.test import Client

from app_book.views import *
from app_user.models import *


class BookTest(TestCase):
    def setUp(self):
        self.user_username = 'test@fixture_mail.com'
        self.user_password = 'supersavepassword'
        self.first_name = 'firstName'
        self.last_name = 'lastName'
        self.username = 'hockeyspieler8'
        with open('fixtures/image1.jpg', 'rb') as img:
            image = SimpleUploadedFile(img.name, img.read(), content_type='image/jpeg')
            self.book_data = {
                'name': 'BookName',
                'author': 'authorName',
                'language': 'Language',
                'releaseDate': '19.11.2016',
                'pageNumber': '13',
                'isbn10': '1-78528-753-2',
                'isbn13': '978-1-78528-753-4',
                'description': 'description',
                'image': image,
            }
        self.offer_data = {
            'price': '3.50',
            'shipping_price': '13.37',
            'active': 'on',
        }
        self.book_offer_data = self.book_data.copy()
        self.book_offer_data.update(self.offer_data)

        self.client = Client()

        user = User.objects.create_user(self.user_username, self.user_password)
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.save()

        status = self.client.login(username=self.user_username, password=self.user_password)
        if status is False:
            raise Exception("Login error")

    def test_seller_search_by_nickname(self):
        users = User.objects.filter(email=self.user_username)
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertIsNone(user.username)
        user.username = self.username
        user.save()
        self.test_create_book_with_Offer()

        response = self.client.get(reverse('app_book:showcases'), data={'seller': self.username})
        #self.assertEqual(len(response.context['users']), 1)
        self.assertEqual(len(response.context['users'].object_list), 1)

    def test_seller_search_by_real_name(self):
        users = User.objects.filter(username=self.username)
        self.assertEqual(len(users), 0)
        self.assertEqual(len(User.objects.filter(first_name=self.first_name)), 1)
        self.assertEqual(len(User.objects.filter(last_name=self.last_name)), 1)

        self.test_create_book_with_Offer()
        response = self.client.get(reverse('app_book:showcases'), data={'seller': self.first_name})
        self.assertEqual(len(response.context['users'].object_list), 1)
        response = self.client.get(reverse('app_book:showcases'), data={'seller': self.last_name})
        self.assertEqual(len(response.context['users'].object_list), 1)



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

        response = self.client.post(reverse('app_book:createBook'), data=data)

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

        response = self.client.put(reverse('app_book:unpublishBook', kwargs={'id': book.first().id}), data=data)

        book = Book.objects.all()
        offer = Offer.objects.all()
        self.assertEqual(len(book), 1, book)
        self.assertEqual(len(offer), 1, offer)
        self.assertEqual(offer[0].active, False, offer)
