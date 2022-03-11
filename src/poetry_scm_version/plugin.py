from cleo.io.io import IO
from poetry.plugins import Plugin
from poetry.poetry import Poetry

from poetry_scm_version import VERSION_STRING
from poetry_scm_version.config import Config


class ScmVersionPlugin(Plugin):
    _config: Config

    def activate(self, poetry: Poetry, io: IO) -> None:
        # Check if we should be active
        version = poetry.pyproject.poetry_config.get("version")
        if version != VERSION_STRING:
            return

        # Version string set, load our config
        self._config = Config.from_project(poetry.pyproject)
