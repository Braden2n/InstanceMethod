"""This module contains the `instancemethod` function that is a higher
order function that can be used as a decorator to prevent methods
from being called from callers that are *not* an instance of the class
that contains the method.

This module also contains the `NotAnInstanceError` error class that is
thrown during invalid calls of a wrapped method.
"""
from inspect import getmembers, getmodule
from typing import Any, Callable
__version__ = "1.4.1"
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
    # Hoisting declarations to highest order scope for performance
    tree = func.__qualname__.split('.')
    module = getmodule(func)
    def instancemethod_wrapper(*args, **kwargs) -> Any:
        """Function wrapper that determines and verifies caller 
        hierarchy prior to method call.

        1. Gets method owners from caller scope using method qualname
        2. Verifies first arg is an instance of the owner class(es)
        3. Returns the function call

        Raises NotAnInstanceError if not all conditions are met.
        """
        # Getting the head owner (index 1) of the first item returned
            # CANNOT BE HOISTED
            # Fails if module finishes load before member declaration
            # Results in IndexError
        owner = getmembers(
            module, lambda o : type(o)==type and o.__name__==tree[0]
        )[0][1]
        # Traversing down attributes to get direct owner
        for attribute in tree[1:-1]: owner = getattr(owner, attribute)
        try:
            self = args[0]
        except IndexError:
            raise NotAnInstanceError(func, owner)
        if not isinstance(self, owner):
            raise NotAnInstanceError(func, owner)
        return func(*args, **kwargs)
    return instancemethod_wrapper
