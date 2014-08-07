from pyramid.httpexceptions import HTTPFound
from .unpackrequest import unpack


class Controller(object):

    def __init__(self, root_factory, request):
        self.request = request
        self.root_factory = root_factory
        unpack(self, request)

        self.before = []
        self.after = []
        self.response = None

    def __call__(self):
        self.before_filter()
        self.data = self.generate_default_data()
        data = self.make() or {}
        self.data.update(data)
        self.after_filter()
        if self.response is None:
            self.make_helpers()
            return self.data
        else:
            return self.response

    def generate_default_data(self):
        return {
            'request': self.request,
            'static': self._get_static_path,
            'route': self.request.route_path,
        }

    def _get_static_path(self, url):
        return self.request.static_path(self.settings['static'] + url)

    def make(self):
        pass

    def before_filter(self):
        for method in self.before:
            method()

    def after_filter(self):
        for method in self.after:
            method()

    def redirect(self, to):
        url = self.request.route_url(to)
        self.response = HTTPFound(location=url)

    def add_helper(self, name, cls, *args, **kwargs):
        self.data[name] = cls(self.request, *args, **kwargs)

    def make_helpers(self):
        pass


class ControllerPlugin(object):

    def __init__(self):
        pass

    def initialize(self, request):
        unpack(self, request)
