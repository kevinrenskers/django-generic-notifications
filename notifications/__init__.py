class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class NotificationEngine(object):
    _types = {}
    _backends = {}

    @classmethod
    def register_backend(cls, backend):
        key = backend.__name__

        if key in cls._backends:
            raise AlreadyRegistered('The notification backend %s is already registered' % key)

        cls._backends[key] = backend

    @classmethod
    def unregister_backend(cls, backend):
        key = backend.__name__

        if key not in cls._backends:
            raise NotRegistered('The notification backend %s is not registered' % key)

        del cls._backends[key]

    @classmethod
    def register_type(cls, type):
        key = type.__name__

        if key in cls._types:
            raise AlreadyRegistered('The notification type %s is already registered' % key)

        cls._types[key] = type

    @classmethod
    def unregister_type(cls, type):
        key = type.__name__

        if key not in cls._types:
            raise NotRegistered('The notification type %s is not registered' % key)

        del cls._types[key]
