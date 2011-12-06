from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from notifications.views import IndexView


urlpatterns = patterns('',
    url(r'^$', login_required(IndexView.as_view()), name='notification-settings-index'),
)
