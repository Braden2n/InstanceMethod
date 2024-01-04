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


@instancemethod
def function() -> bool:
    return True


class TestInstanceMethods(unittest.TestCase):
    def test_class_works(self):
        instance = Class()
        self.assertTrue(instance.method())
        self.assertTrue(Class().method())

    def test_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            Class.method()

    def test_sub_class_works(self):
        instance = SubClass()
        self.assertTrue(instance.method())
        self.assertTrue(SubClass().method())

    def test_sub_class_fails(self):
        with self.assertRaises(NotAnInstanceError):
            SubClass.method()


if __name__ == "__main__":
    unittest.main()