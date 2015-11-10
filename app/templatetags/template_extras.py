# coding=utf-8

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def currency(amount):
    amount = round(float(amount), 2)
    return "%s,%s €" % (intcomma(int(amount)), ("%0.2f" % amount)[-2:])