from django.views.generic import ListView

from shop.models import Product


class ProductList(ListView):
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects \
            .exclude(owner=self.request.user)
        return products
