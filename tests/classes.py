__all__ = [
    "AltClass",
    "Class",
    "SubClass",
    "instancemethod",
    "NotAnInstanceError",
]
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from shutil import rmtree
from typing import Any, Callable
# F-ing ugly import hacking because python sucks >:(
# Required for testing on a machine that also has the package instaled
module_path = Path(__file__).resolve().parents[1] / "src/instancemethod"
# importlib module loading jiggery pokery voodoo magic
spec = spec_from_file_location(
    "instancemethod", 
    (module_path / "__init__.py").absolute()
)
module = module_from_spec(spec)
spec.loader.exec_module(module)
# Getting instance method from loaded package
instancemethod = module.instancemethod
NotAnInstanceError = module.NotAnInstanceError
# rm -rfing unwanted runtime dir caused by exec_module
rmtree((module_path / "__pycache__"))


def null_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Null decorator for more accurate benchmarking."""
    def null_wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)
    return null_wrapper


class Class:
    """Base Class for testing instantiation"""
    def __init__(self) -> None:
        pass

    @instancemethod
    def wrapped_method(self) -> bool:
        """Wrapped method that returns true."""
        return True
    
    @null_decorator
    def unwrapped_method(self) -> bool:
        """Unwrapped method that returns true."""
        return True
    
    class NestedClass:
        """Nested Class for testing attribute nesting"""
        def __init__(self) -> None:
            pass

        @instancemethod
        def wrapped_method(self) -> bool:
            """Wrapped method that returns true."""
            return True
        
        @null_decorator
        def unwrapped_method(self) -> bool:
            """Unwrapped method that returns true."""
            return True
    

class SubClass(Class):
    """Inheriting Class for testing inheritance."""
    pass


class AltClass:
    """Non-inheriting Class for testing fuzzing."""
    def __init__(self) -> None:
        pass
