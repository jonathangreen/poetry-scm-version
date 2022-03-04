from typing import Callable

import pytest
from poetry.core.packages.project_package import ProjectPackage
from poetry.core.version.exceptions import InvalidVersion
from poetry.factory import Factory

from poetry_scm_version.patch import MonkeyPatchPlugin


@pytest.fixture
def test_func() -> Callable[[], ProjectPackage]:
    def run() -> ProjectPackage:
        f = getattr(Factory, MonkeyPatchPlugin.FUNCTION)
        return f("test_package", MonkeyPatchPlugin.VERSION_STRING)

    return run


@pytest.fixture
def patch() -> MonkeyPatchPlugin:
    c = MonkeyPatchPlugin()
    c.activate()
    yield c
    c.deactivate()


def test_normal_exception(test_func):
    with pytest.raises(InvalidVersion):
        test_func()


def test_patch_no_exception(patch, test_func):
    package = test_func()
    assert package.version.text == "0"


def test_deactivate_patch(patch, test_func):
    test_func()
    patch.deactivate()
    with pytest.raises(InvalidVersion):
        test_func()
