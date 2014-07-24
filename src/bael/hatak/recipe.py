from os.path import dirname

from bael.project.recipe import ProjectRecipe
from baelfire.application.application import Application
from baelfire.recipe import Recipe

from .tasks import (
    CreateDataDir,
    Serve,
    MigrationVersioning,
    Migration,
)

from .frontendtask import FrontendIni


class HatakRecipe(Recipe):

    def create_settings(self):
        self.set_path(
            'project:main',
            None,
            dirname(dirname(dirname(__file__))))
        self.set_path('project:src', 'project:main', 'src')
        self.set_path('Hatak', 'project:main', 'Hatak')
        self.set_path('Hatak:src', 'Hatak', 'src')
        self.set_path(
            'templates:frontend.ini',
            None,
            'frontend.ini')
        self.set_path('data', 'project:main', 'data')
        self.set_path('data:frontend.ini', 'data', 'frontend.ini')
        self.set_path('data:log', 'data', 'all.log')
        self.set_path('uwsgi:socket', None, '/tmp/uwsgi.socket')
        self.set_path('uwsgi:socket', None, '/tmp/uwsgi.socket')
        self.set_path(
            'venv:site-packages',
            'virtualenv_path',
            'lib/python3.4/site-packages/')

        self.set_path('flags:dbversioning', 'flags', 'versioning.flag')
        self.set_path('flags:dbmigration', 'flags', 'dbmigration.flag')

        self.set_path('migration:main', 'project:main', 'migrations')
        self.set_path('migration:manage', 'migration:main', 'manage.py')
        self.set_path('migration:versions', 'migration:main', 'versions')

        self.settings['project:name'] = 'KasaMoja'
        self.settings['develop'] = True

    def final_settings(self):
        self.set_path('virtualenv_path', 'project:main', 'venv')
        self.set_path('flags', 'data', 'flags')

    def gather_recipes(self):
        self.add_recipe(ProjectRecipe(False))

    def gather_tasks(self):
        self.add_task(CreateDataDir)
        self.add_task(FrontendIni)
        self.add_task(Serve)
        self.add_task(MigrationVersioning)
        self.add_task(Migration)


def run():
    Application(recipe=HatakRecipe())()
