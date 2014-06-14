from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url('^$',
        'accounts.views.login',
        name='login'),
    url('^logout/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout'),
)
