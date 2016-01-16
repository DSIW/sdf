from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse


from app_book.models import Book, Offer, Counteroffer
from app_user.models import User
from app_notification.models import Notification
from .forms import RateSellerForm
from .models import Payment, SellerRating
from .services import complete_payment, abort_payment, update_payment_from_paypal_ipn, start_payment


def build_payment_form(payment):
    if payment is None:
        return None

    return PayPalPaymentsForm(initial = {
        "business": payment.business,
        "amount": payment.amount,
        "item_name": payment.item_name,
        "invoice": payment.invoice,
        "currency_code": payment.currency_code,
        "notify_url": settings.ENDPOINT + reverse('app_payment:paypal-ipn'),
        "return_url": settings.ENDPOINT + reverse('app_payment:payment-success', kwargs={'id': payment.id}),
        "cancel_return": settings.ENDPOINT + reverse('app_payment:payment-cancel', kwargs={'id': payment.id})
    })

@login_required
def start_paypal_payment(request, id):
    template_name = 'app_payment/payment_start.html'
    try:
        offer = Offer.objects.get(id=id)
    except Offer.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Verkaufsangebot existiert nicht.')
        return HttpResponseRedirect(reverse('app_book:showcases'))

    if offer.seller_user.showcaseDisabled:
        messages.add_message(request, messages.ERROR, 'Das Buch kann nicht gekauft werden, da der Nutzer gesperrt ist!')
        return HttpResponseRedirect(reverse('app_user:user-details', kwargs={'pk': offer.seller_user.id}))

    if not offer.active:
        messages.add_message(request, messages.INFO, 'Das Verkaufsangebot ist nicht aktiv.')
        return HttpResponseRedirect(reverse('app_book:showcases'))

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('app_book:book-detail', kwargs={'id': offer.book.id}))

    if request.user.pk == offer.seller_user.pk:
        messages.add_message(request, messages.INFO, 'Sie können Ihre eigenen Bücher nicht kaufen.')
        return HttpResponseRedirect(reverse('app_book:book-detail', kwargs={'id': offer.book.id}))

    payment = offer.book.active_payment()
    if payment is None:
        payment = Payment()
    success = start_payment(payment, offer, request.current_user, 'fastbuy')

    if success:
        messages.add_message(request, messages.SUCCESS, 'Das Buch ist nun im Bezahlprozess. Sie werden in Kürze zu Paypal weitergeleitet...')
    else:
        messages.add_message(request, messages.ERROR, 'Das Buch ist nicht im Bezahlprozess.')

    return render_to_response(template_name, {
        "payment_form": build_payment_form(payment),
    },  RequestContext(request))


@login_required
def paypal_redirection(request, id):
    template_name = 'app_payment/payment_start.html'

    payment = get_object_or_404(Payment, id=id)

    messages.add_message(request, messages.SUCCESS, 'Sie werden in Kürze zu Paypal weitergeleitet...')

    return render_to_response(template_name, {
        "payment_form": build_payment_form(payment),
    },  RequestContext(request))

@csrf_exempt
@login_required
def paypal_complete(request, id):
    payment = get_object_or_404(Payment, id=id)
    return HttpResponseRedirect(reverse('app_book:book-detail', kwargs={'id': payment.book_id}))

@csrf_exempt
@login_required
def paypal_abort(request, id):
    payment = get_object_or_404(Payment, id=id)
    success = abort_payment(payment)

    if request.method == 'POST' and request.is_ajax():
        return JsonResponse({'result': success})
    else:
        if success:
            messages.add_message(request, messages.SUCCESS, 'Die Bezahlung wurde abgebrochen.')
        return HttpResponseRedirect(reverse('app_book:book-detail', kwargs={'id': payment.book_id}))


def paypal_ipn(sender, **kwargs):
    ipn_obj = sender
    payment = Payment.objects.filter(invoice=ipn_obj.invoice).first()
    if payment is not None:
        update_payment_from_paypal_ipn(payment, ipn_obj)

valid_ipn_received.connect(paypal_ipn)
invalid_ipn_received.connect(paypal_ipn)


@login_required
def rate_seller(request, id):
    backpath = request.META.get('HTTP_REFERER')
    if backpath is None :
        backpath = reverse("app:startPage")
    rating = SellerRating.objects.filter(payment_id=id).first()
    if rating is not None:
        messages.add_message(request,messages.ERROR,"Sie können ein Verkäufer pro Einkauf nur einmal bewerten.")
        return HttpResponseRedirect(backpath)
    payment = get_object_or_404(Payment, id=id)
    if payment is None:
        messages.add_message(request,messages.ERROR,"Sie können diesen Nutzer nicht bewerten.")
        return HttpResponseRedirect(backpath)
    if not payment.is_completed():
        messages.add_message(request,messages.ERROR,"Sie können den Nutzer nur nach abgeschlossenen Käufen bewerten.")
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
            return HttpResponseRedirect(reverse('app_user:user_ratings', kwargs={'pk': rated_user.id}))
        else:
            messages.add_message(request, messages.ERROR, 'Die Bewertung konnte nicht abgegeben werden!')
            return render_to_response('app_payment/rate_seller.html', {'payment': payment, 'form': form}, RequestContext(request))
    else:
        form = RateSellerForm()
        return render_to_response('app_payment/rate_seller.html', {'form': form, 'rating_user': request.user,'rated_user': rated_user,'payment':payment}, RequestContext(request))
