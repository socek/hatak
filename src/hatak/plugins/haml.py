from .plugin import Plugin


class HamlPlugin(Plugin):

    def before_config(self):
        extensions = self.settings.get('jinja2.extensions', [])
        extensions.append('hamlish_jinja.HamlishExtension')
        self.settings['jinja2.extensions'] = extensions

    def add_to_registry(self):
        self.config.add_jinja2_renderer('.haml')
