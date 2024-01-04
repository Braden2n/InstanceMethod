"""This module contains the `instancemethod` function that is a higher
order function that can be used as a decorator to prevent methods
from being called from callers that are *not* an instance of the class
that contains the method.

This module also contains the `NotAnInstanceError` error class that is
thrown during invalid calls of a wrapped method.
"""
from inspect import getmembers, getmodule
from sys import modules
from typing import Any, Callable
__version__ = "1.2.2"
__all__ = [
    "instancemethod",
    "NotAnInstanceError",
]
__refs__ = {
    "AUTHOR": {
        "Name": "Braden Toone",
        "Email": "braden@toonetown.com"
    },
    "HOMEPAGE": "https://github.com/Braden2n/InstanceMethod",
    "DOCUMENTATION": "https://github.com/Braden2n/InstanceMethod",
    "ISSUES": "https://github.com/Braden2n/InstanceMethod/issues",
    "REPOSITORY": "https://github.com",
    "CHANGELOG": "https://github.com/Braden2n/InstanceMethod/activity",
}


class NotAnInstanceError(TypeError):
    """Raised when a method is called without an instantiation of the
    parent class.
    """

    ERR_MSG = (
        "\nThe `{}` method can only be called by an instance of `{}` or one of "
        + "it's subclasses."
    )

    def __init__(self, method: Callable, method_owner: type[object]) -> None:
        super().__init__(
            self.ERR_MSG.format(method.__name__, method_owner.__name__)
        )


def instancemethod(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for limiting method calls to an instance of the class 
    that owns the method. NotAnInstanceError will raise if the caller 
    isn't an instance of the class or any of it's subclasses. 
    instancemethod must be declared the line piror to the method.
    
    Usage:
    __________________________________________________________________
    ### Declaration

    >>> class Foo:
    >>>     def __init__():
    >>>         # Implementation
    >>>         pass
    >>>     
    >>>     @instancemethod
    >>>     def bar():
    >>>         # Implementation
    >>>         pass

    __________________________________________________________________
    ### Valid Call Example

        `foo = Foo()`

        `bar = foo.bar()`

        OR

        `bar = Foo().bar()`

    __________________________________________________________________
    ### Invalid Call Example

        `bar = Foo.bar()`

    >>> `NotAnInstanceError:` '...'

    __________________________________________________________________    
    """
    def predicate(func: Callable[..., Any]) -> Callable[[object], bool]:
        """Function generator that returns a predicate function for
        use with inspect.getmodule.
        """
        def owns_class(object: object) -> bool:
            """Predicate function to determine if an object is a class
            whose name is equal to the owner of a given method.
            """
            return (
                type(object)==type and
                object.__name__==func.__qualname__[0:-1*(len(func.__name__) + 1)]
            )
        return owns_class
    
    def instancemethod_wrapper(*args, **kwargs) -> Any:
        """Function wrapper that determines and verifies caller 
        hierarchy prior to method call.

        1. Gets method owner from caller scope using method qualname
        2. Verifies the first arg is an instance of the owner class
        3. Returns the function call

        Raises NotAnInstanceError if not al conditions are met.
        """
        # Getting the value (index 1) of the first item returned
        method_owner = getmembers(getmodule(func), predicate(func))[0][1]
        try:
            self = args[0]
        except IndexError:
            pass
        else:
            if isinstance(self, method_owner):
                return func(*args, **kwargs)
        raise NotAnInstanceError(func, method_owner)
    return instancemethod_wrapper
