from typing import Any, Callable, Type, TypeVar

T = TypeVar("T", bound="object")

def wrap_function_wrapper(
    module: Type[T], name: str, wrapper: Callable[..., Any]
) -> T: ...

class ObjectProxy:
    __wrapped__: Any
