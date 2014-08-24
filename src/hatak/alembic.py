import sys
from configparser import ConfigParser
from alembic.config import CommandLine

from hatak.application import Application


class AlembicStarter(object):

    def __init__(self, module):
        self.module = module

    def __call__(self):
        self.generate_settings()
        self.generate_config()
        self.add_additional_argv()
        self.run_alembic()

    def generate_settings(self):
        settings, paths = Application.get_settings(self.module)
        merged = settings.merged(paths)
        self.settings = merged.to_dict()

    def generate_config(self):
        config = ConfigParser()
        config['alembic'] = {
            'script_location': self.settings['alembic:versions'],
            'sqlalchemy.url': self.settings['db:url'],
        }
        with open(self.settings['alembic:ini'], 'w') as configfile:
            config.write(configfile)

    def add_additional_argv(self):
        sys.argv.insert(1, '-c')
        sys.argv.insert(2, self.settings['alembic:ini'])
        if 'init' in sys.argv:
            sys.argv.append(self.settings['alembic:versions'])

    def run_alembic(self):
        CommandLine().main()
