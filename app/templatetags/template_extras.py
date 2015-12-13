# -*- coding: utf-8 -*-

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


@register.simple_tag
def url_replace_sort(request, field_by, value_by, field_dir, value_dir):
    request_args = request.GET.copy()
    request_args[field_by] = value_by
    request_args[field_dir] = value_dir
    request_args['page'] = 1
    return request_args.urlencode()


@register.simple_tag
def active(expected, actual):
    if expected == actual:
        return 'active'
    else:
        return ''


@register.filter(name='range')
def times(number):
    return range(number or 0)
