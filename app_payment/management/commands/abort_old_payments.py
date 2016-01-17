from django.core.management.base import BaseCommand, CommandError
from app_payment.models import Payment
from app_payment.services import abort_payment
from paypal.standard.models import *
from django.conf import settings
from datetime import datetime, timedelta

ACTIVE_PAYMENT_STATUSES = [ST_PP_CREATED, ST_PP_ACTIVE, ST_PP_PENDING, ST_PP_VOIDED]

class Command(BaseCommand):
    help = 'Abort all unpaid payments which are older than 30 minutes.'

    def handle(self, *args, **options):
        last_valid_time = datetime.now() - timedelta(seconds=settings.UNPAID_PAYMENT_TIMEOUT)
        payments = Payment.objects.filter(payment_status__in=ACTIVE_PAYMENT_STATUSES, created_at__lte=last_valid_time)

        for payment in payments:
            # remove old payments which were created by fastbuy-button
            if payment.book.source == 'fastbuy':
                abort_payment(payment, notification=True)
                self.stdout.write('Successfully abort payment "%s"' % payment.id)
