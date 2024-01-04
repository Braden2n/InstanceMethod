from unittest import main, TestCase
from classes import AltClass, Class, NotAnInstanceError, SubClass


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
