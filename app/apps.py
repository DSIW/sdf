from django.apps import AppConfig





class ShbAppConfig(AppConfig):
    name = "app"
    def ready(self):
        # imports here to circumvent RemovedInDjango19Warning: Model doesn't declare an explicit app_label
        import watson
        from app.models import Book
        watson.register(Book.objects.filter(isOnStoreWindow=True))