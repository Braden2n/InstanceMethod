"""This module contains the `instancemethod` function that is a higher
order function that can be used as a decorator to prevent methods
from being called from callers that are *not* an instance of the class
that contains the method.

This module also contains the `NotAnInstanceError` error class that is
thrown during invalid calls of a wrapped method.
"""
__all__ = [
    "instancemethod",
    "NotAnInstanceError",
]
from inspect import getmembers
from sys import modules
from typing import Any, Callable


NOT_AN_INSTANCE_ERR_MSG = (
    "\nThe `{}` method can only be called by an instance of `{}` or one of it's"
    + " subclasses."
)


class NotAnInstanceError(TypeError):
    """Raised when a method is called without an instantiation of the
    parent class.
    """

    def __init__(self, method: Callable, method_owner: type[object]) -> None:
        super().__init__(
            NOT_AN_INSTANCE_ERR_MSG.format(
                method.__name__, method_owner.__name__
            )
        )


def instancemethod(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for limiting method calls to an instance of the class 
    that owns the method. NotAnInstanceError will raise if the caller 
    isn't an instance of the class or any of it's subclasses. 
    instancemethod must be declared the line piror to the method.

    *Valid* Example - NotAnInstanceError *ISN'T* Raised
        >>> class Foo:
        >>>     def __init__():
        >>>         ...

        >>>     @instancemethod

        >>>     def bar():
        >>>         ...

        >>> foo = Foo()
        >>> bar = foo.bar()

    *Invalid* Example - NotAnInstanceError *IS* Raised
        >>> class Foo:
        >>>     def __init__():
        >>>         ...

        >>>     @instancemethod

        >>>     def bar():
        >>>         ...

        >>> bar = Foo.bar()
        `NotAnInstanceError:`
        `...`
    """

    def instancemethod_wrapper(*args, **kwargs) -> Any:
        """Function wrapper that determines and verifies caller 
        hierarchy prior to method call.

        1. Gets method owner from caller scope using method qualname
        2. Verifies the first arg is an instance of the owner class
        3. Returns the function call
        """
        # Base case is  _InaccessibleClass if owner not found in loop
        class _InaccessibleClass:
            pass
        method_owner_object = _InaccessibleClass
        # Get owner by func qualname match from caller module objects
        for name, obj in getmembers(modules["__main__"]):
            if name == func.__qualname__[0 : -1 * (len(func.__name__) + 1)]:
                method_owner_object = obj
                break
        # Verify first arg is self
        try:
            self = args[0]
        except IndexError:
            pass
        else:
            if isinstance(self, method_owner_object):
                # Return function call
                return func(*args, **kwargs)
            print(self)
        # Invalid calls exit the try-except-else block and reach here
        raise NotAnInstanceError(func, method_owner_object)
    return instancemethod_wrapper
