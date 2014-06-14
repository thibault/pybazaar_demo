from django.conf.urls import patterns, url

from shop.views import ProductList


urlpatterns = patterns(
    '',
    url('^$',
        ProductList.as_view(),
        name='shop'),
)
