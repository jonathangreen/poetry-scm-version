from typing import Callable, Dict, Tuple, Type

import wrapt
from cleo.io.io import IO
from poetry.console.application import Application
from poetry.core.packages.project_package import ProjectPackage
from poetry.core.semver.version import Version
from poetry.factory import Factory
from poetry.plugins import ApplicationPlugin, Plugin
from poetry.poetry import Poetry


def wrapper(
    wrapped: Callable[[str, str], ProjectPackage],
    instance: Type,
    args: Tuple[str, str],
    kwargs: Dict,
) -> ProjectPackage:
    name, version = args
    if version == "scm-version":
        parsed_version = Version.from_parts(0)
        return ProjectPackage(name, parsed_version, version)
    else:
        return wrapped(name, version)


class ScmPatchPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        wrapt.wrap_function_wrapper(Factory, "get_package", wrapper)


class ScmVersionPlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO):
        print("there")
