from django.views.generic.base import TemplateView
from notifications.engine import NotificationEngine


class IndexView(TemplateView):
    template_name = 'notifications/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['notification_types'] = NotificationEngine._types
        return context
