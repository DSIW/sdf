from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def currency(amount):
    amount = round(float(amount), 2)
    return "%s,%s €" % (intcomma(int(amount)), ("%0.2f" % amount)[-2:])


@register.simple_tag
def url_replace(request, field, value):
    request_args = request.GET.copy()
    request_args[field] = value
    return request_args.urlencode()