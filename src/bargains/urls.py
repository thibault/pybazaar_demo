from django.conf.urls import patterns, url

from bargains.views import BargainCreate, Bargain


urlpatterns = patterns(
    '',
    url('^create/$',
        BargainCreate.as_view(),
        name='bargain_init'),
    url('^(?P<pk>\d+)/$',
        Bargain.as_view(),
        name='bargain'),
)
