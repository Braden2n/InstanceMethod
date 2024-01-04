from timeit import timeit
from unittest import main, TestCase
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
        def wrapped_method(self) -> bool:
            return True
        
        def unwrapped_method(self) -> bool:
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

BEST_BENCHMARK_WRAPPED_COMPARISON = 225
BENCHMARK_ASSERTION_THRESHHOLD = BEST_BENCHMARK_WRAPPED_COMPARISON * 1.5


def bulk_time(func: Callable, times: int = 1_000_000) -> float:
    return timeit(func, number=times)


def time_instance(instance: object) -> tuple[float]:
    wrapped = bulk_time(instance.wrapped_method)
    unwrapped = bulk_time(instance.unwrapped_method)
    return (wrapped, unwrapped)


def wrap_comparison(title: str, wrapped: float, unwrapped: float) -> float:
    slower = 1/(unwrapped/wrapped)
    print(f"\n\n{title}")
    print("\tWrapped", "{:.3f}".format(wrapped), "microseconds/call")
    print("\tUnwrapped", "{:.3f}".format(unwrapped), "microseconds/call")
    print("\tWrapped is", "{:.0f}x".format(slower), "slower")
    return slower


class TestFunctionality(TestCase):
    wrapped_results = []
    unwrapped_results = []
    def test_a_time_classes(self):
        wrapped, unwrapped = time_instance(Class())
        self.wrapped_results.append(wrapped)
        self.unwrapped_results.append(unwrapped)
        slower = wrap_comparison("Instancing:", wrapped, unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHHOLD)

    def test_b_time_sub_classes(self):
        wrapped, unwrapped = time_instance(SubClass())
        self.wrapped_results.append(wrapped)
        self.unwrapped_results.append(unwrapped)
        slower = wrap_comparison("Inherited Instancing:", wrapped, unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHHOLD)

    def test_c_time_nested_classes(self):
        wrapped, unwrapped = time_instance(Class.NestedClass())
        self.wrapped_results.append(wrapped)
        self.unwrapped_results.append(unwrapped)
        slower = wrap_comparison("Nested Class Instancing:", wrapped, unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHHOLD)
    
    def test_z_time_benchmark_results(self):
        slower = wrap_comparison("Overall:", self.wrapped, self.unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHHOLD)

    @property
    def wrapped(self) -> float:
        return sum(self.wrapped_results) / len(self.wrapped_results)
    
    @property
    def unwrapped(self) -> float:
        return sum(self.unwrapped_results) / len(self.unwrapped_results)
        

if __name__ == "__main__":
    main()
