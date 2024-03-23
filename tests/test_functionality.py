from unittest import TestCase, main

from src.instancemethod import NotAnInstanceError
from .classes import (
    ChildDeclares, ChildDeclaresExternal, ChildInherits, Empty, OuterClass,
    ParentDeclares,
    )


FUZZING_TYPES: list[object] = [
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
    Empty(),
    ]


class TestFunctionality(TestCase):

    def test_method_works(self) -> None:
        self.assertTrue(ParentDeclares().wrapped_method())
        self.assertTrue(ParentDeclares.wrapped_method(ParentDeclares()))

    def test_method_fails(self) -> None:
        with self.assertRaises(NotAnInstanceError):
            ParentDeclares.wrapped_method()  # type: ignore
        for test_type in FUZZING_TYPES:
            with self.assertRaises(NotAnInstanceError):
                ParentDeclares.wrapped_method(test_type)  # type: ignore

    def test_inheritance_works(self) -> None:
        self.assertTrue(ChildInherits().wrapped_method())
        self.assertTrue(
            ChildInherits.wrapped_method(ChildInherits())
            )

    def test_inheritance_fails(self) -> None:
        with self.assertRaises(NotAnInstanceError):
            ChildInherits.wrapped_method()  # type: ignore
        for test_type in FUZZING_TYPES:
            with self.assertRaises(NotAnInstanceError):
                ChildInherits.wrapped_method(test_type)  # type: ignore

    def test_polymorphism_works(self) -> None:
        self.assertTrue(ChildDeclares().wrapped_method())
        self.assertTrue(ChildDeclares.wrapped_method(ChildDeclares()))
        self.assertTrue(ChildDeclaresExternal().wrapped_method())
        self.assertTrue(
            ChildDeclaresExternal.wrapped_method(ChildDeclaresExternal())
            )

    def test_polymorphism_fails(self) -> None:
        with self.assertRaises(NotAnInstanceError):
            ChildDeclares.wrapped_method()  # type: ignore
        for test_type in FUZZING_TYPES:
            with self.assertRaises(NotAnInstanceError):
                ChildDeclares.wrapped_method(test_type)  # type: ignore

    def test_overriding_works(self) -> None:
        self.assertTrue(ChildDeclares().wrapped_method())
        self.assertTrue(ChildDeclares.wrapped_method(ChildDeclares()))

    def test_overriding_fails(self) -> None:
        with self.assertRaises(NotAnInstanceError):
            ChildDeclares.wrapped_method()  # type: ignore
        for test_type in FUZZING_TYPES:
            with self.assertRaises(NotAnInstanceError):
                ChildDeclares.wrapped_method(test_type)  # type: ignore

    def test_attribution_works(self) -> None:
        self.assertTrue(OuterClass.NestedClass().wrapped_method())
        self.assertTrue(
            OuterClass.NestedClass.wrapped_method(
                OuterClass.NestedClass()
                )
            )

    def test_attribution_fails(self) -> None:
        with self.assertRaises(NotAnInstanceError):
            OuterClass.NestedClass.wrapped_method()  # type: ignore
        with self.assertRaises(NotAnInstanceError):
            OuterClass().NestedClass.wrapped_method()  # type: ignore
        for test_type in FUZZING_TYPES:
            with self.assertRaises(NotAnInstanceError):
                OuterClass.NestedClass.wrapped_method(
                    test_type  # type: ignore
                    )
            with self.assertRaises(NotAnInstanceError):
                OuterClass().NestedClass.wrapped_method(
                    test_type  # type: ignore
                    )


if __name__ == "__main__":
    main()
