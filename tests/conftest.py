import pytest

from poetry_scm_version.patch import MonkeyPatchPlugin


@pytest.fixture(autouse=True)
def unpatch():
    yield
    MonkeyPatchPlugin.deactivate()
