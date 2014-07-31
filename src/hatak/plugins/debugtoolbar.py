from .plugin import Plugin


class DebugtoolbarPlugin(Plugin):

    def get_include_name(self):
        return 'pyramid_debugtoolbar'
