from django.conf.urls import patterns, url

from shop.views import ProductList, Bargain


urlpatterns = patterns(
    '',
    url('^$',
        ProductList.as_view(),
        name='shop'),
    url('^(?P<pk>\d+)/$',
        Bargain.as_view(),
        name='bargain'),
)
