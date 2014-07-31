from .plugin import Plugin


class Jinja2Plugin(Plugin):

    def get_include_name(self):
        return 'pyramid_jinja2'

    def add_to_registry(self):
        self.registry['jinja2'] = self.config.get_jinja2_environment()
