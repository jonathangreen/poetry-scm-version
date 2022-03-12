from typing import Generator

import pytest

from poetry_scm_version.patch import MonkeyPatchPlugin


@pytest.fixture(autouse=True)
def unpatch() -> Generator[None, None, None]:
    yield
    MonkeyPatchPlugin.deactivate()
