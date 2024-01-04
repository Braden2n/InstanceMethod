import unittest
if __name__ == "__main__":
    from sys import path
    path.insert(0, "../src/instancemethod.py")
from instancemethod import instancemethod, NotAnInstanceError


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
