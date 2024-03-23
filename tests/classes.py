from typing import Any, Callable, Iterable, Iterator

from src.instancemethod import instancemethod


def null_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Null decorator for more accurate higher-order function benchmarks"""

    def null_wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return null_wrapper


class ParentDeclares:

    def __init__(self) -> None:
        pass

    @instancemethod
    def wrapped_method(self) -> bool:
        return True

    @null_decorator
    def unwrapped_method(self) -> bool:
        return True


class Empty:

    def __init__(self) -> None:
        pass


class ChildInherits(ParentDeclares):
    pass


class ChildDeclares(Empty):

    @instancemethod
    def wrapped_method(self) -> bool:
        return True

    @null_decorator
    def unwrapped_method(self) -> bool:
        return True


class ChildDeclaresExternal(Iterable[Any]):

    def __iter__(self) -> Iterator[Any]:
        return iter("")

    @instancemethod
    def wrapped_method(self) -> bool:
        return True

    @null_decorator
    def unwrapped_method(self) -> bool:
        return True


class ChildOverrides(ParentDeclares):

    @instancemethod
    def wrapped_method(self) -> bool:
        return False

    @null_decorator
    def unwrapped_method(self) -> bool:
        return False


class OuterClass:

    def __init__(self) -> None:
        pass

    class NestedClass:

        def __init__(self) -> None:
            pass

        @instancemethod
        def wrapped_method(self) -> bool:
            return True

        @null_decorator
        def unwrapped_method(self) -> bool:
            return True
