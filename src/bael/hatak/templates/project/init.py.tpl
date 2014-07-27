from hatak.application import Application

from .routes import make_routes

main = Application(make_routes)
