from typing import (
    Any,
    Callable,
    List,
    Mapping,
    Optional,
    Type,
)

import wrapt
from poetry.console.application import Application
from poetry.core.factory import Factory as CoreFactory
from poetry.core.packages.project_package import ProjectPackage
from poetry.factory import Factory as PoetryFactory
from poetry.plugins import ApplicationPlugin

from poetry_scm_version import VERSION_STRING


class MonkeyPatchPoetry:
    FUNCTION: str = "get_package"

    @staticmethod
    def wrapper(
        wrapped: Callable[[], ProjectPackage],
        instance: object,
        args: List[str],
        kwargs: Mapping[str, Any],
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
            return ProjectPackage(name, "0", version)
        else:
            return wrapped(*args, **kwargs)

    @classmethod
    def patch(cls, patch_cls: Type[CoreFactory]) -> None:
        wrapt.wrap_function_wrapper(patch_cls, cls.FUNCTION, cls.wrapper)

    @classmethod
    def unpatch(cls, patch_cls: Type[CoreFactory]) -> None:
        # Unpatch method. This is only used in the context of tests.
        f = getattr(patch_cls, cls.FUNCTION, None)
        if (
            f is not None
            and isinstance(f, wrapt.ObjectProxy)
            and hasattr(f, "__wrapped__")
        ):
            setattr(patch_cls, cls.FUNCTION, f.__wrapped__)


class MonkeyPatchPlugin(ApplicationPlugin):
    # We need to define an application plugin, because we need to patch poetry.core before
    # it is loaded, and normal plugins are loaded too late for that. This plugin does the patching
    # but the bulk of the work for versioning is handled by ScmVersionPlugin.

    def activate(self, application: Optional[Application] = None) -> None:
        # Poetry doesn't provide a clean method to change how the version property is
        # handled, so we patch it here. This is kind of ugly, but we do our best to
        # keep the patching to a minimum.
        MonkeyPatchPoetry.patch(PoetryFactory)

    @staticmethod
    def deactivate() -> None:
        MonkeyPatchPoetry.unpatch(PoetryFactory)
