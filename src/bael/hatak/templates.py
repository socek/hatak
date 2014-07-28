from os import path

from baelfire.template import TemplateTask


class MigrationManage(TemplateTask):

    def get_output_file(self):
        return self.paths['migration:manage']

    def get_template_path(self):
        return 'manage2.py.tpl'

    def generate_links(self):
        self.add_link('bael.project.tasks:GatherData')
        self.add_link('bael.hatak.tasks:MigrationData')


class InitPy(TemplateTask):

    def get_template_path(self):
        return path.join('project/init.py.tpl')

    def get_output_file(self):
        return self.paths['project:initpy']


class Routes(TemplateTask):

    def get_template_path(self):
        return path.join('project/routes.py.tpl')

    def get_output_file(self):
        return self.paths['project:routes']


class Settings(TemplateTask):

    def get_template_path(self):
        return path.join('project/settings.py.tpl')

    def get_output_file(self):
        return self.paths['project:default']