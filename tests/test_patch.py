from typing import (
    Any,
    Callable,
    Generator,
    List,
    Mapping,
)

import pytest
from poetry.core.packages.project_package import ProjectPackage
from poetry.core.version.exceptions import InvalidVersion
from poetry.factory import Factory

from poetry_scm_version import VERSION_STRING
from poetry_scm_version.patch import (
    MonkeyPatchPlugin,
    MonkeyPatchPoetry,
)


@pytest.fixture
def test_func() -> Callable[[], ProjectPackage]:
    def run() -> ProjectPackage:
        f = getattr(Factory, MonkeyPatchPoetry.FUNCTION)
        return f("test_package", VERSION_STRING)

    return run


@pytest.fixture
def patch() -> Generator[MonkeyPatchPlugin, None, None]:
    c = MonkeyPatchPlugin()
    c.activate()
    yield c
    c.deactivate()


def test_normal_exception(test_func: Callable[[], ProjectPackage]) -> None:
    with pytest.raises(InvalidVersion):
        test_func()


def test_patch_no_exception(
    patch: MonkeyPatchPlugin, test_func: Callable[[], ProjectPackage]
) -> None:
    package = test_func()
    assert package.version.text == "0"


def test_deactivate_patch(
    patch: MonkeyPatchPlugin, test_func: Callable[[], ProjectPackage]
) -> None:
    test_func()
    patch.deactivate()
    with pytest.raises(InvalidVersion):
        test_func()


@pytest.mark.parametrize(
    "args, kwargs",
    [
        (["test", "scm"], {}),
        (["test"], {"version": "scm"}),
        ([], {"name": "test", "version": "scm"}),
    ],
)
def test_args(
    patch: MonkeyPatchPlugin, args: List[str], kwargs: Mapping[str, Any]
) -> None:
    f = getattr(Factory, MonkeyPatchPoetry.FUNCTION)
    package = f(*args, **kwargs)
    assert package.name == "test"
    assert package.version.text == "0"
