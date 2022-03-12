import datetime as dt
import os
import re
from importlib import import_module
from typing import Optional

import jinja2
from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from dunamai import _VERSION_PATTERN, Style, Vcs
from dunamai import Version as DVersion
from dunamai import (
    bump_version,
    check_version,
    serialize_pep440,
    serialize_pvp,
    serialize_semver,
)
from poetry.core.semver.version import Version
from poetry.plugins import Plugin
from poetry.poetry import Poetry

from poetry_scm_version import VERSION_STRING
from poetry_scm_version.config import Config


class ScmVersionPlugin(Plugin):
    _config: Config

    @staticmethod
    def _escape_branch(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return re.sub(r"[^a-zA-Z0-9]", "", value)

    @staticmethod
    def _format_timestamp(value: Optional[dt.datetime]) -> Optional[str]:
        if value is None:
            return None
        return value.strftime("%Y%m%d%H%M%S")

    def get_version(self) -> str:
        vcs = Vcs(self._config.vcs)
        if self._config.style is not None:
            style = Style(self._config.style)
        else:
            style = None
        pattern = self._config.pattern or _VERSION_PATTERN
        version = DVersion.from_vcs(vcs, pattern, self._config.latest_tag)
        bump = self._config.bump and version.distance > 0

        if self._config.format_jinja:
            if bump:
                version = version.bump()
            default_context = {
                "base": version.base,
                "version": version,
                "stage": version.stage,
                "revision": version.revision,
                "distance": version.distance,
                "commit": version.commit,
                "dirty": version.dirty,
                "branch": version.branch,
                "branch_escaped": self._escape_branch(version.branch),
                "timestamp": self._format_timestamp(version.timestamp),
                "env": os.environ,
                "bump_version": bump_version,
                "tagged_metadata": version.tagged_metadata,
                "serialize_pep440": serialize_pep440,
                "serialize_pvp": serialize_pvp,
                "serialize_semver": serialize_semver,
            }
            custom_context = {}
            if self._config.format_jinja_imports is not None:
                for entry in self._config.format_jinja_imports:
                    module = import_module(entry["module"])
                    if "item" in entry:
                        custom_context[entry["item"]] = getattr(module, entry["item"])
                    else:
                        custom_context[entry["module"]] = module
            serialized = jinja2.Template(self._config.format_jinja).render(
                **default_context, **custom_context
            )
            if style is not None:
                check_version(serialized, style)
        else:
            # These type ignores are necessary because upstream library does not
            # properly annotate these variables as Optional, when they do actually
            # take None as a possible argument.
            serialized = version.serialize(
                metadata=self._config.metadata,  # type: ignore
                dirty=self._config.dirty,
                format=self._config.format,  # type: ignore
                style=style,  # type: ignore
                bump=bump,
                tagged_metadata=self._config.tagged_metadata,
            )

        return serialized

    def activate(self, poetry: Poetry, io: IO) -> None:
        # Check if we should be active
        project_version = poetry.pyproject.poetry_config.get("version")
        if project_version != VERSION_STRING:
            return

        io.output.write(
            "<comment><info>Scm-version</info> plugin active.</comment>",
            new_line=True,
            verbosity=Verbosity.VERBOSE,
        )

        # Version string set, load our config
        self._config = Config.from_project(poetry.pyproject)

        # Get correct version based on config
        version_string = self.get_version()
        io.output.write(
            f"<comment>Version set to <info>{version_string}</info>.</comment>",
            new_line=True,
            verbosity=Verbosity.VERBOSE,
        )
        version_obj = Version.parse(version_string)
        poetry.package.set_version(version_obj)
