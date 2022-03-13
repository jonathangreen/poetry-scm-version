from pathlib import Path
from typing import (
    Callable,
    List,
)

import entrypoints
import poetry
import pytest
from _pytest.monkeypatch import MonkeyPatch
from cleo.testers.application_tester import ApplicationTester
from poetry.console.application import Application
from poetry.plugins.plugin_manager import PluginManager
from pyfakefs.fake_filesystem import FakeFilesystem


@pytest.fixture
def fixture() -> Callable[[str], Path]:
    def get_data(fixture: str) -> Path:
        fixture_dir = Path(__file__).parent / "fixtures"
        fixture_file = fixture_dir / fixture
        return fixture_file

    return get_data


@pytest.fixture(autouse=True)
def poetry_path(fs: FakeFilesystem) -> FakeFilesystem:
    [fs.add_real_directory(path) for path in poetry.__path__]
    return fs


@pytest.fixture
def pyproject(
    fs: FakeFilesystem, fixture: Callable[[str], Path], monkeypatch: MonkeyPatch
) -> Path:
    path = Path("/fake/path")
    project = path / "pyproject.toml"
    fs.add_real_file(fixture("scm.toml"), False, project)
    monkeypatch.chdir(path)
    return path


@pytest.fixture
def patch_poetry_plugin_loader(monkeypatch: MonkeyPatch) -> None:
    def get_plugin(self: PluginManager) -> List[entrypoints.EntryPoint]:
        if self._type == "application.plugin":
            return [
                entrypoints.EntryPoint.from_string(
                    "poetry_scm_version.patch:MonkeyPatchPlugin", "poetry-scm-version"
                )
            ]
        else:
            return []

    monkeypatch.setattr(PluginManager, "get_plugin_entry_points", get_plugin)


def test_poetry_fails_no_plugin(pyproject: Path) -> None:
    tester = ApplicationTester(Application())
    tester.execute(args="version")
    assert "InvalidVersion" in tester.io.fetch_error()
    assert tester.status_code != 0


def test_poetry_with_plugin(pyproject: Path, patch_poetry_plugin_loader: None) -> None:
    tester = ApplicationTester(Application())
    tester.execute(args="version")
    assert "InvalidVersion" not in tester.io.fetch_error()
    assert tester.status_code == 0
