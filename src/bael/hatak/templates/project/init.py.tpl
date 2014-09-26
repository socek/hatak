from hatak.application import Application
from hatak.plugins import DebugtoolbarPlugin, TosterPlugin
from hatak.plugins import StaticPlugin, BeakerPlugin, HamlPlugin, AlembicPlugin
from hatak.plugins import SqlPlugin
from hatak.logging import LoggingPlugin
from hatak.jinja2 import Jinja2Plugin


from {{settings["package:name"]}}.application.tests.fixtures import Fixtures
from .routes import make_routes

main = Application('{{settings["package:name"]}}', make_routes)
main.add_plugin(LoggingPlugin())
main.add_plugin(Jinja2Plugin())
main.add_plugin(HamlPlugin())
main.add_plugin(SqlPlugin())
main.add_plugin(AlembicPlugin())
main.add_plugin(BeakerPlugin())
main.add_plugin(DebugtoolbarPlugin())
main.add_plugin(TosterPlugin(Fixtures))
main.add_plugin(StaticPlugin())
