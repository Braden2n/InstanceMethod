from timeit import timeit
from typing import Callable
from unittest import main, TestCase
from classes import Class, SubClass


# Decorated Microseconds/call: 3.85
# Null-Decorated Microseconds/Call: 0.08
BEST_BENCHMARK_WRAPPED_COMPARISON = 46
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
    print("\tWrapped", "{:.4f}".format(wrapped), "microseconds/call")
    print("\tUnwrapped", "{:.4f}".format(unwrapped), "microseconds/call")
    print("\tWrapped is", "{:.2f}x".format(slower), "slower")
    return slower


class TestPerformance(TestCase):
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
