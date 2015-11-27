from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import json


from app_book.models import Book, Offer
from app_user.models import User
from .models import Payment
from .services import complete_payment, abort_payment, update_payment_from_paypal_ipn

def start_paypal_payment(request, id):
    template_name = 'app_payment/payment_start.html'

    if request.method != 'POST':
        raise BaseException('Use POST request for starting payments.')

    offer = Offer.objects.filter(id=id).first()
    buyer = request.user

    payment = Payment()
    payment.init_process(offer, buyer)
    payment.save()

    form = PayPalPaymentsForm(initial = {
        "business": payment.business,
        "amount": payment.amount,
        "item_name": payment.item_name,
        "invoice": payment.invoice,
        "currency_code": payment.currency_code,
        "notify_url": settings.ENDPOINT + reverse('app_payment:paypal-ipn'),
        "return_url": settings.ENDPOINT + reverse('app_payment:payment-success', kwargs={'id': payment.id}),
        "cancel_return": settings.ENDPOINT + reverse('app_payment:payment-cancel', kwargs={'id': payment.id}),
        "custom": payment.custom
    })

    messages.add_message(request, messages.SUCCESS, 'Das Buch ist nun im Bezahlprozess. Sie werden in Kürze zu Paypal weitergeleitet...')

    return render_to_response(template_name, {
        "payment_form": form,
    },  RequestContext(request))

@csrf_exempt
def paypal_complete(request, id):
    payment = Payment.objects.filter(id=id).first()
    complete_payment(payment)
    messages.add_message(request, messages.SUCCESS, 'Die Paypal-Transaktion wurde durchgeführt. Bitte prüfen Sie, ob das Geld bei Ihnen angekommen ist.')
    return render(request, "app_payment/payment_success.html")

@csrf_exempt
def paypal_abort(request, id):
    payment = Payment.objects.filter(id=id).first()
    abort_payment(payment)
    messages.add_message(request, messages.ERROR, 'Die Paypal-Transaktion wurde abgebrochen.')
    return render(request, "app_payment/payment_cancel.html")

# Get new status info from paypal
def paypal_ipn(sender, **kwargs):
    ipn_obj = sender
    payment_id = json.loads(ipn_obj.custom)['payment_id']
    payment = Payment.objects.filter(id=payment_id).first()
    print('>>> New paypal status: '+sender.payment_status)
    update_payment_from_paypal_ipn(payment, ipn_obj)

valid_ipn_received.connect(paypal_ipn)
