# coding=utf-8

from django.views.generic.base import TemplateView

class StartPageView(TemplateView):
    template_name = 'app/start.html'

    def get_context_data(self, **kwargs):
        context = super(StartPageView, self).get_context_data(**kwargs)
        return context

