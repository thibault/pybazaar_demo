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

    def post(self, *args, **kwargs):
        price = int(self.request.POST.get('price'))
        memo = self.request.POST.get('memo')
        bargain = self.get_object()
        bargain.create_message(self.request.user, price, memo)

        return http.HttpResponseRedirect(bargain.get_absolute_url())
