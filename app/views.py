# coding=utf-8

from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

class StartPageView(TemplateView):
    template_name = 'app/start.html'

    def get_context_data(self, **kwargs):
        context = super(StartPageView, self).get_context_data(**kwargs)
        return context

def page_info(request, template_name, title):
    return render_to_response(template_name, {"title":title}, RequestContext(request))
