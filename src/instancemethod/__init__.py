"""This module contains the `instancemethod` function that is a higher
order function that can be used as a decorator to prevent methods
from being called from callers that are *not* an instance of the class
that contains the method.

This module also contains the `NotAnInstanceError` error class that is
thrown during invalid calls of a wrapped method.
"""
from functools import lru_cache
from inspect import getmembers, getmodule
from typing import Any, Callable, TypeVar, cast


__version__ = "2.0"
__all__ = [
    "instancemethod",
    "NotAnInstanceError",
    "FailedInstanceCheckError",
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

F = TypeVar("F", bound=Callable[..., Any])


class NotAnInstanceError(TypeError):
    """Raised when a method is called without an instantiation of the
    parent class.
    """

    ERR_MSG = (
            "\nThe `{}` method can only be called by an instance of `{}` or "
            "one of "
            + "it's subclasses."
    )

    def __init__(self, method: F, method_owner: type) -> None:
        super().__init__(
            self.ERR_MSG.format(method.__name__, method_owner.__name__)
            )


class FailedInstanceCheckError(TypeError):
    """Raised when a method is not able to be instance checked."""

    ERR_MSG = (
        "\nThe `{}` failed the instance check. Reach out to the code "
        "developers with a bug report."
    )

    def __init__(self, method: F) -> None:
        super().__init__(self.ERR_MSG.format(method.__name__))


@lru_cache
def get_members_from_func(func: F) -> tuple[list[tuple[str, type]], list[str]]:
    """Function for inspecting a function scope to retrieve local
    members. Returns a tuple of members and the qualified name tree."""
    # Getting string representation of ownership tree
    tree: list[str] = func.__qualname__.split('.')
    # Getting the module where the function was defined
    module = getmodule(func)
    # Getting the static members of the module
    # The predicate used filters by the function name
    members = getmembers(
        module, lambda o: isinstance(o, type) and o.__name__ == tree[0]
        )
    # members will be empty if the function is a closure or out of scope
    if not members:
        if func.__closure__ is not None:
            # Function is a closure and can be passed recursively
            closure = func.__closure__[0].cell_contents
            return get_members_from_func(closure)
        # Function is out of scope and impossible to check
        raise FailedInstanceCheckError(func)
    return members, tree


@lru_cache
def get_owner_from_func(func: F) -> type:
    """Function for returning a function's owner from any module."""
    # Gets local scope of function and a tree representing the qualname
    members, tree = get_members_from_func(func)
    # Accessing the first object in the list of tuples
    owner = members[0][1]
    # Traversing down attributes to get highest-level owner
    for attribute in tree[1:-1]:
        # Types do not have a <local> attribute - which is always called
        if isinstance(owner, type) and not attribute == '<locals>':
            # Getting next step in attribute tree for nested classes
            owner = getattr(owner, attribute)
    return owner


def instancemethod(func: F) -> F:
    """Decorator for limiting method calls to an instance of the class
    that owns the method. NotAnInstanceError will raise if the caller
    isn't an instance of the class or any of its subclasses.
    instancemethod must be declared the line prior to the method.
    FailedInstanceCheckError will raise if the function is impossible
    to check due to not existing in the inspected scope.

    Usage:
    __________________________________________________________________
    ### Declaration

    ```python
    class Foo(optional Inheritance):
        def __init__(self): ...

        @instancemethod
        def bar(self): ...
    ```

    __________________________________________________________________
    ### Valid Call Example

    ```python
    foo = Foo()
    foo.bar()
    ```

        OR

    ```python
    Foo().bar()
    ```

    __________________________________________________________________
    ### Invalid Call Example

    ```python
    Foo.bar()
    ```

    `NotAnInstanceError: '...'`

    __________________________________________________________________
    """

    def instancemethod_wrapper(*args: Any, **kwargs: Any) -> Any:
        """Function wrapper that determines and verifies caller
        hierarchy prior to method call.

        1. Gets method owner from the function
        2. Verifies first arg is an instance of the owner.
        3. Makes the function call

        Raises NotAnInstanceError if not all conditions are met.
        Raises FailedInstanceCheckError if function is uncheckable.
        """
        # All instance methods pass the instance object to a method
        try:
            # Getting method owner for instance checking
            owner = get_owner_from_func(func)
        except FailedInstanceCheckError:
            raise FailedInstanceCheckError(func)
        try:
            # Getting first (self) arg
            self = args[0]
        except IndexError:
            # No args were passed - invalid behavior
            raise NotAnInstanceError(func, owner)
        if not isinstance(self, owner):
            # 'self' is not an instance - invalid behavior
            raise NotAnInstanceError(func, owner)
        return func(*args, **kwargs)

    return cast(F, instancemethod_wrapper)
