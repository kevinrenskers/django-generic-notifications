from django.conf.urls.defaults import patterns, url
from notifications.views import IndexView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='notification-settings-index'),
)
