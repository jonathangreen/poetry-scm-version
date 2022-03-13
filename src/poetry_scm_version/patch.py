from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
)

import wrapt
from poetry.console.application import Application
from poetry.core.packages.project_package import ProjectPackage
from poetry.factory import Factory
from poetry.plugins import ApplicationPlugin

from poetry_scm_version import VERSION_STRING


class MonkeyPatchPlugin(ApplicationPlugin):
    # We need to define an application plugin, because we need to patch poetry.core before
    # it is loaded, and normal plugins are loaded too late for that. This plugin does the patching
    # but the bulk of the work for versioning is handled by ScmVersionPlugin.
    FUNCTION: str = "get_package"

    @staticmethod
    def get_package_wrapper(
        wrapped: Callable[[str, str], ProjectPackage],
        instance: object,
        args: List[str],
        kwargs: Dict[str, Any],
    ) -> ProjectPackage:
        if len(args) > 0:
            name = args[0]
        elif "name" in kwargs:
            name = kwargs["name"]
        else:
            name = None

        if len(args) > 1:
            version = args[1]
        elif "version" in kwargs:
            version = kwargs["version"]
        else:
            version = None

        if version == VERSION_STRING:
            return ProjectPackage(name, "0", "0")
        else:
            return wrapped(*args, **kwargs)

    def activate(self, application: Optional[Application] = None) -> None:
        # Poetry doesn't provide a clean method to change how the version property is
        # handled, so we patch it here. This is kind of ugly, but we do our best to
        # keep the patching to a minimum.
        wrapt.wrap_function_wrapper(Factory, self.FUNCTION, self.get_package_wrapper)

    @classmethod
    def deactivate(cls) -> None:
        # Unpatch method. This is only used in the context of tests currently.
        f = getattr(Factory, cls.FUNCTION, None)
        if (
            f is not None
            and isinstance(f, wrapt.ObjectProxy)
            and hasattr(f, "__wrapped__")
        ):
            setattr(Factory, cls.FUNCTION, f.__wrapped__)
