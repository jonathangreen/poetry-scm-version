from cleo.io.io import IO
from poetry.poetry import Poetry

from .base_plugin import BasePlugin as BasePlugin

class Plugin(BasePlugin):
    type: str
    def activate(self, poetry: Poetry, io: IO) -> None: ...
