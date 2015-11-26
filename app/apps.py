# -*- coding: utf-8 -*-

from django.apps import AppConfig


class ShbAppConfig(AppConfig):
    name = "app"

    def ready(self):
        # imports here to circumvent RemovedInDjango19Warning: Model doesn't declare an explicit app_label
        import watson
        from app_book.models import Book, Offer
        from app_user.models import User

        disabledShowcases = User.objects.filter(showcaseDisabled=True).values_list('user_ptr')
        bookIds = Offer.objects.exclude(seller_user_id__in=disabledShowcases).values_list('book', flat=True)
        watson.register(Book.objects.filter(id__in=bookIds))
