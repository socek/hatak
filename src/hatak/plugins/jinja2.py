from .plugin import Plugin


class Jinja2Plugin(Plugin):

    def get_include_name(self):
        return 'pyramid_jinja2'

    def add_to_registry(self):
        self.registry['jinja2'] = self.config.get_jinja2_environment()


class Jinja2Helper(object):

    def __init__(self, request):
        self.request = request
        self.registry = request.registry
        self.generate_data()

    def generate_data(self):
        self.data = {
            'request': self.request,
            'registry': self.registry,
        }

    def get_template(self):
        return self.template

    def render(self, template):
        env = self.registry['jinja2']
        template = env.get_template(template)
        return template.render(**self.data)

    def __call__(self):
        self.make()
        return self.render(self.get_template())

    def make(self):
        pass
