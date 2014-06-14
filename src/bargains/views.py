from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse
from django import http

from bargains.models import Bargain


class BargainCreate(CreateView):
    model = Bargain
    fields = ['product', 'buyer']

    def form_invalid(self, form):
        url = reverse('shop')
        return http.HttpResponseRedirect(url)


class Bargain(DetailView):
    template_name = 'bargains/bargain.html'
    model = Bargain
    context_object_name = 'bargain'
