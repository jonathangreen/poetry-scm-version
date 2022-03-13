from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from dunamai import (
    _VERSION_PATTERN,
    Style,
    Vcs,
    Version as DunamiVersion,
)
from poetry.core.semver.version import Version
from poetry.plugins import Plugin
from poetry.poetry import Poetry

from poetry_scm_version import VERSION_STRING
from poetry_scm_version.config import Config


class ScmVersionPlugin(Plugin):
    _config: Config
    _io: IO

    def get_version(self) -> str:
        vcs = Vcs(self._config.vcs)
        style = Style(self._config.style) if self._config.style is not None else None
        pattern = self._config.pattern or _VERSION_PATTERN

        try:
            version = DunamiVersion.from_vcs(vcs, pattern, self._config.latest_tag)
            bump = self._config.bump and version.distance > 0
            serialized = version.serialize(
                metadata=self._config.metadata,
                dirty=self._config.dirty,
                format=self._config.format,
                style=style,
                bump=bump,
                tagged_metadata=self._config.tagged_metadata,
            )
        except (RuntimeError, ValueError) as e:
            if self._config.default is not None:
                serialized = self._config.default
                self._io.error_output.write(
                    f"<warning>Scm-version: {e}</warning>", new_line=True
                )
                self._io.output.write(
                    f"<comment>Falling back to default version: <info>{serialized}</info></comment>",
                    new_line=True,
                )
            else:
                raise e

        return serialized

    def activate(self, poetry: Poetry, io: IO) -> None:
        # Check if we should be active
        project_version = poetry.pyproject.poetry_config.get("version")
        if project_version != VERSION_STRING:
            return

        self._io = io

        self._io.output.write(
            "<comment><info>Scm-version</info> plugin active</comment>",
            new_line=True,
            verbosity=Verbosity.VERBOSE,
        )

        # Version string set, load our config
        self._config = Config.from_project(poetry.pyproject)

        # Get correct version based on config
        version_string = self.get_version()
        self._io.output.write(
            f"<comment>Version set to <info>{version_string}</info></comment>",
            new_line=True,
            verbosity=Verbosity.VERBOSE,
        )
        version_obj = Version.parse(version_string)
        poetry.package.set_version(version_obj)
