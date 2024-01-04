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
# rm -rfing unwanted runtime dir caused by exec_module
rmtree((module_path / "__pycache__"))


BEST_BENCHMARK_WRAPPED_COMPARISON = 225
BENCHMARK_ASSERTION_THRESHHOLD = BEST_BENCHMARK_WRAPPED_COMPARISON * 1.5


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
