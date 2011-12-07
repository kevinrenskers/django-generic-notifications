from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from notifications.engine import NotificationEngine
from notifications.models import DisabledNotificationsTypeBackend


class IndexView(TemplateView):
    template_name = 'notifications/index.html'

    def get_context_data(self, **kwargs):
        disabled_backends = {}

        for obj in DisabledNotificationsTypeBackend.objects.filter(user=self.request.user):
            disabled_backends[obj.notification_type] = obj.get_backends()

        notification_types = {}
        for class_name, type_class in NotificationEngine._types.items():
            notification_types[class_name] = {
                'type_class': type_class,
                'disabled_backends': disabled_backends.get(class_name, [])
            }

        context = super(IndexView, self).get_context_data(**kwargs)
        context['notification_types'] = notification_types
        context['notification_backends'] = NotificationEngine._backends
        return context

    def post(self, request, **kwargs):
        DisabledNotificationsTypeBackend.objects.filter(user=request.user).delete()

        for type_name, type_class in NotificationEngine._types.items():
            allowed_backends = type_class().allowed_backends
            enabled_backends = request.POST.getlist(type_name)

            # Subtract the enabled backends from allowed_backends, the difference is disabled_backends
            disabled_backends = list(allowed_backends)
            [disabled_backends.remove(x) for x in enabled_backends]

            if disabled_backends:
                DisabledNotificationsTypeBackend.objects.create(
                    user = request.user,
                    notification_type = type_name,
                    notification_backends = ','.join(disabled_backends)
                )

        messages.success(request, 'Your notification settings have been saved')
        return HttpResponseRedirect(reverse('notification-settings-index'))
