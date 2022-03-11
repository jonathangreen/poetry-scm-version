from typing import Callable, Dict, Optional, Tuple, Type

import wrapt
from poetry.console.application import Application
from poetry.core.packages.project_package import ProjectPackage
from poetry.factory import Factory
from poetry.plugins import ApplicationPlugin

from poetry_scm_version import VERSION_STRING


class MonkeyPatchPlugin(ApplicationPlugin):
    FUNCTION: str = "get_package"

    @staticmethod
    def get_package_wrapper(
        wrapped: Callable[[str, str], ProjectPackage],
        instance: Type,
        args: Tuple[str, str],
        kwargs: Dict,
    ) -> ProjectPackage:
        name, version = args
        if version == VERSION_STRING:
            version = "0"
        return wrapped(name, version)

    def activate(self, application: Optional[Application] = None):
        wrapt.wrap_function_wrapper(Factory, self.FUNCTION, self.get_package_wrapper)

    @classmethod
    def deactivate(cls):
        f = getattr(Factory, cls.FUNCTION, None)
        if (
            f is not None
            and isinstance(f, wrapt.ObjectProxy)
            and hasattr(f, "__wrapped__")
        ):
            setattr(Factory, cls.FUNCTION, f.__wrapped__)
