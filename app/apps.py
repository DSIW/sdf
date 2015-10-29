from django.apps import AppConfig


class ShbAppConfig(AppConfig):
    name = "app"

    def ready(self):
        # imports here to circumvent RemovedInDjango19Warning: Model doesn't declare an explicit app_label
        import watson
        from app.models import Book, Offer

        bookIds = Offer.objects.values_list('book', flat=True)

        watson.register(Book.objects.filter(id__in=bookIds))