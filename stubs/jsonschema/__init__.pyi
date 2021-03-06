import abc
from typing import (
    Any,
    ClassVar,
    Iterator,
    Type,
    TypeVar,
)

T = TypeVar("T", bound="_Error")

class _Error(Exception):
    message: str
    path: str
    schema_path: str
    context: Any
    cause: Any
    validator: Any
    validator_value: Any
    instance: dict[str, Any]
    schema: dict[str, Any]
    parent: Any
    # def __init__(self, message, validator=..., path=..., cause: Any | None = ..., context=..., validator_value=..., instance=..., schema=..., schema_path=..., parent: Any | None = ...) -> None: ...
    @classmethod
    def create_from(cls: Type[T], other: Exception) -> T: ...
    @property
    def absolute_path(self) -> str: ...
    @property
    def absolute_schema_path(self) -> str: ...
    @property
    def json_path(self) -> str: ...

class ValidationError(_Error): ...

class Validator(metaclass=abc.ABCMeta):
    META_SCHEMA: ClassVar[Any]
    VALIDATORS: ClassVar[Any]
    TYPE_CHECKER: ClassVar[Any]
    schema: Any
    def __init__(
        self, schema: dict[str, Any], resolver: Any = ..., format_checker: Any = ...
    ) -> None: ...
    @classmethod
    def check_schema(cls, schema: dict[str, Any]) -> None: ...
    def is_type(self, instance: dict[str, Any], type: str) -> bool: ...
    def is_valid(self, instance: dict[str, Any]) -> bool: ...
    def iter_errors(self, instance: dict[str, Any]) -> Iterator[ValidationError]: ...
    def validate(self, instance: dict[str, Any]) -> None: ...
    def evolve(self, **kwargs: dict[str, Any]) -> Validator: ...

class Draft7Validator(Validator): ...
