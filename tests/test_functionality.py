import unittest
if __name__ != "__main__":
    from instancemethod import instancemethod, NotAnInstanceError
else:
    # F-ing ugly import hacking because python sucks >:(
    from importlib.util import spec_from_file_location, module_from_spec
    from pathlib import Path
    from shutil import rmtree
    from typing import Any, Callable
    module_path = Path(__file__).resolve().parents[1] / "src/instancemethod"
    # importlib loading jiggery pokery voodoo magic
    spec = spec_from_file_location(
        "instancemethod", 
        (module_path / "__init__.py").absolute()
    )
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    # naming used vars
    instancemethod: Callable[[Callable[..., Any]], Callable[..., Any]] = module\
        .instancemethod
    NotAnInstanceError: TypeError = module.NotAnInstanceError
    # rm-ing unwanted runtime dir caused by exec_module
    rmtree((module_path / "__pycache__"))


class Class:
    def __init__(self) -> None:
        pass

    @instancemethod
    def method(self) -> bool:
        return True
    
    class NestedClass:
        def __init__(self) -> None:
            pass

        @instancemethod
        def nested_method(self) -> bool:
            return True
    

class SubClass(Class):
    pass


class AltClass:
    def __init__(self) -> None:
        pass


TYPES = [
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


class TestFunctionality(unittest.TestCase):
    def test_class_works(self):
        self.assertTrue(Class().method())

    def test_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            Class.method()
        for test_type in TYPES:
            with self.assertRaises(NotAnInstanceError):
                Class.method(test_type)

    def test_sub_class_works(self):
        self.assertTrue(SubClass().method())

    def test_sub_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            SubClass.method()
        for test_type in TYPES:
            with self.assertRaises(NotAnInstanceError):
                SubClass.method(test_type)

    def test_nested_class_works(self):
        self.assertTrue(Class().NestedClass().nested_method())

    def test_nested_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            Class.NestedClass.nested_method()
        with self.assertRaises(NotAnInstanceError):
            Class().NestedClass.nested_method()
        for test_type in TYPES:
            with self.assertRaises(NotAnInstanceError):
                Class.NestedClass.nested_method(test_type)
            with self.assertRaises(NotAnInstanceError):
                Class().NestedClass.nested_method(test_type)
        

if __name__ == "__main__":
    unittest.main()
