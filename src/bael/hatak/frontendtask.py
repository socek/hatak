from baelfire.template import TemplateTask


class FrontendIni(TemplateTask):
    name = 'Creating frontend.ini file'
    path = '/hatak/frontend.ini'

    def generate_links(self):
        super().generate_links()
        self.add_link('bael.hatak.tasks:CreateDataDir')

    def get_output_file(self):
        return self.paths['data:frontend.ini']

    def get_template_path(self):
        return self.paths['templates:frontend.ini']
