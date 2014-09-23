from hatak.plugins import Plugin
from .commands import AlembicCommand


class AlembicPlugin(Plugin):

    def add_commands(self, parent):
        parent.add_command(AlembicCommand())
