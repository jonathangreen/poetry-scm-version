from typing import Any, Callable, Mapping
from unittest.mock import create_autospec

import pytest
from tomlkit.toml_document import TOMLDocument

from poetry_scm_version.config import CONFIG_KEY, Config


@pytest.fixture
def load_config() -> Callable[[Mapping[str, Any]], Config]:
    def load(data: Mapping[str, Any]) -> Config:
        def make_config(key: str, data: Mapping[str, Any]):
            sep = "."
            if sep in key:
                [current, next] = key.split(".", 1)
                return {current: make_config(next, data)}
            else:
                return {key: data}

        document = create_autospec(TOMLDocument)
        type(document).data = make_config(CONFIG_KEY, data)
        return Config.from_project(document)

    return load


@pytest.mark.parametrize(
    "param,value",
    [
        ("vcs", "git"),
        ("vcs", "any"),
        ("vcs", "mercurial"),
        ("vcs", "darcs"),
        ("vcs", "bazaar"),
        ("vcs", "subversion"),
        ("vcs", "fossil"),
        ("default", "test"),
        ("pattern", "test"),
        ("metadata", True),
        ("tagged-metadata", True),
        ("dirty", True),
        ("format", "test"),
        ("format-jinja", "test"),
        ("style", "pep440"),
        ("style", "semver"),
        ("style", "pvp"),
        ("latest-tag", True),
        ("bump", True),
    ],
)
def test_config(load_config, param, value):
    c = load_config({param: value})
    assert getattr(c, param.replace("-", "_")) == value


@pytest.mark.parametrize(
    "param,default",
    [
        ("vcs", "any"),
        ("default", None),
        ("pattern", None),
        ("metadata", None),
        ("tagged-metadata", False),
        ("dirty", False),
        ("format", None),
        ("format-jinja", None),
        ("style", None),
        ("latest-tag", False),
        ("bump", False),
    ],
)
def test_config_default(load_config, param, default):
    c = load_config({})
    assert getattr(c, param.replace("-", "_")) == default


@pytest.mark.parametrize(
    "config", [{"vcs": "invalid"}, {"style": "foo"}, {"format": "test", "dirty": True}]
)
def test_config_exception(load_config, config):
    with pytest.raises(RuntimeError):
        load_config(config)
