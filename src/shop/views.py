from django.views.generic import ListView, DetailView

from shop.models import Product


class ProductList(ListView):
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects \
            .exclude(owner=self.request.user)
        return products


class Bargain(DetailView):
    template_name = 'shop/bargain.html'
