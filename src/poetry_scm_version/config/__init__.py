import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Mapping, Optional, Sequence, Type, TypeVar

from jsonschema import Draft7Validator
from poetry.core.pyproject.toml import PyProjectTOML
from tomlkit.toml_document import TOMLDocument

SCHEMA_FILE: str = "schema.json"
CONFIG_KEY: str = "tool.poetry-scm-version"

T = TypeVar("T", bound="Config")


@dataclass
class Config:
    default: Optional[str] = None
    pattern: Optional[str] = None
    metadata: Optional[bool] = None
    format: Optional[str] = None
    format_jinja: Optional[str] = None
    format_jinja_imports: Optional[Sequence[Mapping[str, str]]] = None
    style: Optional[str] = None
    vcs: str = "any"
    latest_tag: bool = False
    bump: bool = False
    tagged_metadata: bool = False
    dirty: bool = False

    @classmethod
    def from_project(cls: Type[T], project: PyProjectTOML) -> T:
        config = project.data
        for key in CONFIG_KEY.split("."):
            config = config.get(key, {})

        errors = cls.validate(config)
        if len(errors) != 0:
            message = ""
            for error in errors:
                message += f"  - {error}\n"
            raise RuntimeError(
                "The Poetry SCM Version configuration is invalid:\n" + message
            )

        config_dict = {k.replace("-", "_"): v for k, v in config.items()}
        return cls(**config_dict)

    @staticmethod
    def _format_error(message: str, path: Optional[str] = None) -> str:
        if path:
            error_path = [CONFIG_KEY]
            error_path.extend(path)
            message = "[{}] {}".format(".".join(str(x) for x in error_path), message)
        return message

    @classmethod
    def validate(cls, config: TOMLDocument) -> List[str]:
        schema_file = Path(__file__).parent / SCHEMA_FILE
        if not schema_file.exists():
            raise ValueError("poetry_scm_version schema does not exist.")

        schema = json.loads(schema_file.read_text())

        validator = Draft7Validator(schema)
        validation_errors = sorted(validator.iter_errors(config), key=lambda e: e.path)

        errors = [
            cls._format_error(error.message, error.absolute_path)
            for error in validation_errors
        ]

        if "format" in config or "format-jinja" in config:
            for prop in ["metadata", "tagged-metadata", "dirty"]:
                if prop in config:
                    errors.append(
                        cls._format_error(
                            "Not allowed when 'format' or 'format-jinja' is also defined.",
                            prop,
                        )
                    )

        if "format" in config and "format-jinja" in config:
            errors.append(
                cls._format_error(
                    "Only one of 'format' or 'format-jinja' can be defined.", "format"
                )
            )

        if "format-jinja-imports" in config and "format-jinja" not in config:
            errors.append(
                cls._format_error("'format-jinja' not defined.", "format-jinja-imports")
            )

        return errors
