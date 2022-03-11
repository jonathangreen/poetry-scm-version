from types import SimpleNamespace

from cleo.io.io import IO
from poetry.core.pyproject.toml import PyProjectTOML
from poetry.plugins import Plugin
from poetry.poetry import Poetry

from poetry_scm_version import VERSION_STRING


class ScmVersionPlugin(Plugin):
    CONFIG_KEY: str = "tool.poetry-scm-version"

    def __init__(self):
        self.config = SimpleNamespace()

    def load_config(self, toml: PyProjectTOML):
        config = toml.data
        for key in self.CONFIG_KEY.split("."):
            if config is not None:
                config = config.get(key)

        self.config.vcs = config.get("vcs", "any")
        self.config.metadata = config.get("metadata", False)

        return config

    def activate(self, poetry: Poetry, io: IO):
        # Check if we should be active
        version = poetry.pyproject.poetry_config.get("version")
        if version != VERSION_STRING:
            return

        # Version string set, load our config
        self.load_config(poetry.pyproject)
