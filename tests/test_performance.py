from timeit import timeit
from unittest import TestCase, main
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
    def wrapped_method(self) -> bool:
        return True
    
    def unwrapped_method(self) -> bool:
        return True
    
    class NestedClass:
        def __init__(self) -> None:
            pass

        @instancemethod
        def wrapped_nested_method(self) -> bool:
            return True
        
        def unwrapped_nested_method(self) -> bool:
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


class TestFunctionality(TestCase):
    def test_class_differende(self):
        time1 = timeit(Class().wrapped_method, number=10_000)
        print("class_wrapped_time", "{:.16f}".format(time1 / 10_000), "seconds/call")
        time2 = timeit(Class().unwrapped_method, number=10_000)
        print("class_unwrapped_time", "{:.16f}".format(time2 / 10_000), "seconds/call")
        print("Unrapped advantage:", "{:.2f}".format(1/(time2 / time1)))
        self.assertLess(1 / (time2 / time1), 15_000)

    def test_sub_class_wrapped_time(self):
        time1 = timeit(SubClass().wrapped_method, number=10_000)
        print("sub_class_wrapped_time", "{:.16f}".format(time1 / 10_000, "seconds/call"))
        time2 = timeit(SubClass().unwrapped_method, number=10_000)
        print("sub_class_unwrapped_time", "{:.16f}".format(time2 / 10_000, "seconds/call"))
        print("Unrapped advantage:", "{:.2f}".format(1/(time2 / time1)))
        self.assertLess(1 / (time2 / time1), 15_000)

    def test_nested_class_wrapped_time(self):
        time1 = timeit(Class().NestedClass().wrapped_nested_method, number=10_000)
        print("nested_class_wrapped_time", "{:.16f}".format(time1 / 10_000, "seconds/call"))
        time2 = timeit(Class().NestedClass().unwrapped_nested_method, number=10_000)
        print("nested_class_unwrapped_time", "{:.16f}".format(time2 / 10_000, "seconds/call"))
        print("Unrapped advantage:", "{:.2f}".format(1/(time2 / time1)))
        self.assertLess(1 / (time2 / time1), 15_000)
        

if __name__ == "__main__":
    main()
