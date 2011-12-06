from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from notifications.engine import NotificationEngine
from notifications.models import SelectedNotificationsType


class IndexView(TemplateView):
    template_name = 'notifications/index.html'

    def get_context_data(self, **kwargs):
        selected_backends = {}

        for obj in SelectedNotificationsType.objects.filter(user=self.request.user):
            selected_backends[obj.notification_type] = obj.get_backends()

        notification_types = {}
        for class_name, type_class in NotificationEngine._types.items():
            notification_types[class_name] = {
                'type_class': type_class,
                'selected_backends': selected_backends.get(class_name, [])
            }

        context = super(IndexView, self).get_context_data(**kwargs)
        context['notification_types'] = notification_types
        context['notification_backends'] = NotificationEngine._backends
        return context

    def post(self, request, **kwargs):
        SelectedNotificationsType.objects.filter(user=request.user).delete()

        for type_name in NotificationEngine._types.keys():
            backends = request.POST.getlist(type_name)

            if backends:
                SelectedNotificationsType.objects.create(
                    user = request.user,
                    notification_type = type_name,
                    notification_backends = ','.join(backends)
                )

        messages.success(request, 'Your notification settings have been saved')
        return HttpResponseRedirect(reverse('notification-settings-index'))
