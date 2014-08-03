from pyramid.config import Configurator
from smallsettings import Factory

from .plugins import Jinja2Plugin, SqlPlugin, BeakerPlugin, DebugtoolbarPlugin
from .plugins import LoggingPlugin


class Application(object):

    """Prepering and configuring project."""

    def __init__(self, module, make_routes):
        self.make_routes = make_routes
        self.module = module
        self.plugins = []
        self.generate_plugins()

    def generate_plugins(self):
        self.add_plugin(LoggingPlugin())
        self.add_plugin(Jinja2Plugin())
        self.add_plugin(SqlPlugin())
        self.add_plugin(BeakerPlugin())
        self.add_plugin(DebugtoolbarPlugin())

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
        plugin.init(self)

    def __call__(self, settings={}):
        self.settings = self.generate_settings(settings)
        self.make_before_config()
        self.create_config()
        self.make_pyramid_includes()
        self.make_routes(self)
        self.make_registry()

        return self.config.make_wsgi_app()

    def generate_settings(self, settings):
        self._settings, self._paths = self.get_settings(self.module, settings)
        merged = self._settings.merged(self._paths)
        return merged.to_dict()

    @classmethod
    def get_settings(cls, module, settings={}):
        factory = Factory('%s.application' % (module))
        settings, paths = factory.make_settings(
            settings=settings,
            additional_modules=[
                ('local', False),
            ])
        return settings, paths

    def create_config(self):
        self.config = Configurator(
            settings=self.settings,
        )

    def make_before_config(self):
        for plugin in self.plugins:
            plugin.before_config()

    def make_pyramid_includes(self):
        for plugin in self.plugins:
            plugin.make_config_include_if_able()
        self.config.commit()

    def make_registry(self):
        self.config.registry['settings'] = self.settings
        for plugin in self.plugins:
            plugin.add_to_registry()
