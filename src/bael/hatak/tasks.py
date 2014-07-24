from os import mkdir, path
from glob import glob

from bael.project.virtualenv import VirtualenvTask
from baelfire.dependencies import (
    AlwaysRebuild,
    FileDoesNotExists,
    FileChanged,
)
from baelfire.error import CommandError
from baelfire.task import Task


class CreateDataDir(Task):
    name = 'Creating data directory'
    path = '/hatak/data'

    directorie_names = [
        'data',
    ]

    @property
    def directories(self):
        for name in self.directorie_names:
            yield self.paths[name]

    def generate_dependencies(self):
        for directory in self.directories:
            self.add_dependecy(FileDoesNotExists(directory))

    def make(self):
        for directory in self.directories:
            if not path.exists(directory):
                mkdir(directory)


class Serve(Task):
    name = 'Run development server'
    path = '/hatak/serve'

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        self.add_link('bael.hatak.frontendtask:FrontendIni')
        self.add_link('bael.project.virtualenv:Develop')
        self.add_link(Migration)

    def make(self):
        self.command(['pserve %(data:frontend.ini)s --reload' % (self.paths)])


class Migration(VirtualenvTask):

    def migration(self, command, *args, **kwargs):
        command = self.paths['migration:manage'] + ' ' + command
        return self.python(command, *args, **kwargs)


class MigrationVersioning(Migration):
    path = '/hatak/migration/versioning'

    def get_output_file(self):
        return self.paths['flags:dbversioning']

    def generate_links(self):
        self.add_link('bael.hatak.frontendtask:FrontendIni')
        self.add_link('bael.project.virtualenv:Develop')

    def make(self):
        try:
            self.migration('version_control')
        except CommandError:
            pass
        self.touchme()


class Migration(Migration):
    path = '/hatak/migration'

    def generate_dependencies(self):
        super().generate_dependencies()
        for file_ in glob(path.join(self.paths['migration:versions'], '*.py')):
            self.add_dependecy(FileChanged(file_))

    def get_output_file(self):
        return self.paths['flags:dbmigration']

    def generate_links(self):
        self.add_link(MigrationVersioning)

    def make(self):
        self.migration('upgrade')
        self.touchme()
