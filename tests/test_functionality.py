import unittest
import sys
sys.path.insert(0, "../src/instancemethod.py")
from instancemethod import instancemethod, NotAnInstanceError


class Class:
    def __init__(self) -> None:
        pass
    
    @instancemethod
    def method(self) -> bool:
        return True


class SubClass(Class):
    pass


class AltClass:
    def __init__(self) -> None:
        pass


TEST_TYPES = [
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

class TestInstanceMethods(unittest.TestCase):
    def test_class_works(self):
        instance = Class()
        self.assertTrue(instance.method())
        self.assertTrue(Class().method())

    def test_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            Class.method()
        for test_type in TEST_TYPES:
            with self.assertRaises(NotAnInstanceError):
                Class.method(test_type)

    def test_sub_class_works(self):
        instance = SubClass()
        self.assertTrue(instance.method())
        self.assertTrue(SubClass().method())

    def test_sub_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            SubClass.method()
        for test_type in TEST_TYPES:
            with self.assertRaises(NotAnInstanceError):
                SubClass.method(test_type)


if __name__ == "__main__":
    unittest.main()