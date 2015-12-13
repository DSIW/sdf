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
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import json


from app_book.models import Book, Offer, Counteroffer
from app_user.models import User
from app_notification.models import Notification
from .forms import RateSellerForm
from .models import Payment,SellerRating
from .services import complete_payment, abort_payment, update_payment_from_paypal_ipn

@login_required
def start_paypal_payment(request, id):
    template_name = 'app_payment/payment_start.html'

    offer = Offer.objects.get(id=id)

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('app_book:book-detail', kwargs={'id': offer.book.id}))

    payment = Payment()
    payment.init_process(offer, request.current_user)
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

@login_required
def start_paypal_payment_by_counter_offer(request, id):
    template_name = 'app_payment/payment_start.html'

    counter_offer = Counteroffer.objects.get(id=id)

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('app_book:book-detail', kwargs={'id': counter_offer.offer.book.id}))

    payment = Payment()
    payment.init_process(counter_offer.offer, request.current_user)
    payment.amount = counter_offer.price
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
@login_required
def paypal_complete(request, id):
    payment = Payment.objects.filter(id=id).first()
    Notification.request_rating(payment)
    complete_payment(payment)
    messages.add_message(request, messages.SUCCESS, 'Die Paypal-Transaktion wurde durchgeführt.')
    return render(request, "app_payment/payment_success.html")

@csrf_exempt
@login_required
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


@login_required
def rate_seller(request, id):
    backpath = request.META.get('HTTP_REFERER')
    if backpath is None :
        backpath = reverse("app:startPage")
    rating = SellerRating.objects.filter(payment_id=id).first()
    if rating is not None:
        messages.add_message(request,messages.ERROR,"Sie können ein Verkäufer pro Einkauf nur einmal bewerten.")
        return HttpResponseRedirect(backpath)
    payment = Payment.objects.filter(pk=id).first()
    if payment is None:
        messages.add_message(request,messages.ERROR,"Sie können diesen Nutzer nicht bewerten.")
        return HttpResponseRedirect(backpath)
    rated_user = User.objects.filter(pk=payment.seller_user.id).first()
    if request.method == 'POST':
        form = RateSellerForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.payment = payment
            form.instance.rated_user = rated_user
            form.instance.rating_user = User.objects.filter(pk=request.user.id).first()
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Vielen Dank, Ihre Bewertung wurde gespeichert!')
            return HttpResponseRedirect(reverse('app_book:showcase', kwargs={'user_id': rated_user.id}))
        else :
            messages.add_message(request, messages.SUCCESS, 'Die Bewertung konnte nicht abgespeichert werden.')
            return render_to_response('app_payment/rate_seller.html', {'form': form, 'rated_user': rated_user, 'rating_user': request.user}, RequestContext(request))
    else:
        form = RateSellerForm()
        return render_to_response('app_payment/rate_seller.html', {'form': form, 'rating_user': request.user,'rated_user': rated_user,'payment':payment}, RequestContext(request))
