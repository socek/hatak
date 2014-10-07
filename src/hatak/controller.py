from pyramid.httpexceptions import HTTPFound
from .unpackrequest import unpack


class EndController(Exception):
    pass


class Controller(object):

    def __init__(self, root_factory, request):
        self.request = request
        self.root_factory = root_factory
        unpack(self, request)

        self.response = None
        self.initialize_plugins()

    def __call__(self):
        try:
            self.before_filter()
            self.data = self.generate_default_data()
            data = self.make() or {}
            self.data.update(data)
            self.after_filter()
            if self.response is None:
                self.make_helpers()
                self.make_plugin_helpers()
                return self.data
            else:
                return self.response
        except EndController:
            return self.response

    def generate_default_data(self):
        data = {
            'request': self.request,
            'route': self.request.route_path,
        }
        for plugin in self.plugins:
            plugin.generate_default_data(data)
        return data

    def make(self):
        pass

    def initialize_plugins(self):
        self.plugins = []
        for plugin in self.registry['controller_plugins']:
            self.plugins.append(plugin(self))

    def before_filter(self):
        for plugin in self.plugins:
            plugin.before_filter()

    def after_filter(self):
        for plugin in self.plugins:
            plugin.after_filter()

    def redirect(self, to):
        url = self.request.route_url(to)
        self.response = HTTPFound(location=url)

    def add_helper(self, name, cls, *args, **kwargs):
        self.data[name] = cls(self.request, *args, **kwargs)

    def make_helpers(self):
        pass

    def make_plugin_helpers(self):
        for plugin in self.plugins:
            plugin.make_helpers()


class ControllerPlugin(object):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.request = self.controller.request
        unpack(self, self.request)
        self.add_helper = self.controller.add_helper
        self.add_controller_methods()

    def add_controller_methods(self):
        pass

    def add_method(self, name):
        method = getattr(self, name)
        setattr(self.controller, name, method)

    def before_filter(self):
        pass

    def after_filter(self):
        pass

    def generate_default_data(self, data):
        pass

    def make_helpers(self):
        pass
