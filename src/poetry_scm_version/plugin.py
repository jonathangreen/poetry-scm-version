from cleo.io.io import IO
from poetry.plugins import Plugin
from poetry.poetry import Poetry


class ScmVersionPlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO):
        print("there")
