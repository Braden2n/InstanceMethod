from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from shutil import rmtree
from timeit import timeit
from typing import Callable
from unittest import main, TestCase
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


class Class:
    """Base Class for testing instantiation"""
    def __init__(self) -> None:
        pass

    @instancemethod
    def wrapped_method(self) -> bool:
        """Wrapped method that returns true."""
        return True
    
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


FUZZING_TYPES = [
    None,
    int(),
    float(),
    complex(),
    str(),
    list(),
    tuple(),
    range(0),
    bytes(),
    bytearray(),
    memoryview(bytes(0)),
    dict(),
    bool(),
    set(),
    frozenset(),
    AltClass(),
]


class TestFunctionality(TestCase):
    def test_class_works(self):
        self.assertTrue(Class().wrapped_method())
        self.assertTrue(Class.wrapped_method(Class()))

    def test_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            Class.wrapped_method()
        for test_type in FUZZING_TYPES:
            with self.assertRaises(NotAnInstanceError):
                Class.wrapped_method(test_type)

    def test_sub_class_works(self):
        self.assertTrue(SubClass().wrapped_method())
        self.assertTrue(SubClass.wrapped_method(SubClass()))

    def test_sub_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            SubClass.wrapped_method()
        for test_type in FUZZING_TYPES:
            with self.assertRaises(NotAnInstanceError):
                SubClass.wrapped_method(test_type)

    def test_nested_class_works(self):
        self.assertTrue(Class.NestedClass().wrapped_method())
        self.assertTrue(Class.NestedClass.wrapped_method(Class.NestedClass()))

    def test_nested_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            Class.NestedClass.wrapped_method()
        with self.assertRaises(NotAnInstanceError):
            Class().NestedClass.wrapped_method()
        for test_type in FUZZING_TYPES:
            with self.assertRaises(NotAnInstanceError):
                Class.NestedClass.wrapped_method(test_type)
            with self.assertRaises(NotAnInstanceError):
                Class().NestedClass.wrapped_method(test_type)
        

if __name__ == "__main__":
    main()
