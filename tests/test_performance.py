from timeit import timeit
from typing import Any, Callable
from unittest import TestCase, main

from .classes import (
    ChildDeclaresExternal, ChildInherits, ChildOverrides, OuterClass,
    ParentDeclares,
    )


# Decorated Nanoseconds/call: 138.381
# Null-Decorated Nanoseconds/Call: 85
BEST_BENCHMARK_WRAPPED_COMPARISON = 1.65
BENCHMARK_ASSERTION_THRESHOLD = BEST_BENCHMARK_WRAPPED_COMPARISON * 1.5


def bulk_time(func: Callable[..., Any], times: int = 1_000_000) -> float:
    return timeit(func, number=times)


Testable = (ChildDeclaresExternal | ChildInherits | OuterClass.NestedClass |
            ParentDeclares | ChildOverrides)


def time_instance(instance: Testable) -> (
        tuple)[float, float]:
    wrapped = bulk_time(instance.wrapped_method) * 1000
    unwrapped = bulk_time(instance.unwrapped_method) * 1000
    return wrapped, unwrapped


def wrap_comparison(title: str, wrapped: float, unwrapped: float) -> float:
    slower = 1 / (unwrapped / wrapped)
    print(f"\n\n{title}")
    print("\tWrapped", "{:.3f}".format(wrapped), "Nanoseconds/call")
    print("\tUnwrapped", "{:.3f}".format(unwrapped), "Nanoseconds/call")
    print("\tWrapped is", "{:.2f}x".format(slower), "slower")
    return slower


class TestPerformance(TestCase):
    wrapped_results: list[float] = []
    unwrapped_results: list[float] = []

    def test_a_time_classes(self) -> None:
        wrapped, unwrapped = time_instance(ParentDeclares())
        self.wrapped_results.append(wrapped)
        self.unwrapped_results.append(unwrapped)
        slower = wrap_comparison("Instancing:", wrapped, unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHOLD)

    def test_b_time_sub_classes(self) -> None:
        wrapped, unwrapped = time_instance(ChildInherits())
        self.wrapped_results.append(wrapped)
        self.unwrapped_results.append(unwrapped)
        slower = wrap_comparison("Inherited Instancing:", wrapped, unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHOLD)

    def test_c_time_sub_classes(self) -> None:
        wrapped, unwrapped = time_instance(ChildDeclaresExternal())
        self.wrapped_results.append(wrapped)
        self.unwrapped_results.append(unwrapped)
        slower = wrap_comparison("Polymorphic Instancing:", wrapped, unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHOLD)

    def test_d_time_sub_classes(self) -> None:
        wrapped, unwrapped = time_instance(ChildOverrides())
        self.wrapped_results.append(wrapped)
        self.unwrapped_results.append(unwrapped)
        slower = wrap_comparison("Overriden Instancing:", wrapped, unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHOLD)

    def test_e_time_nested_classes(self) -> None:
        wrapped, unwrapped = time_instance(OuterClass.NestedClass())
        self.wrapped_results.append(wrapped)
        self.unwrapped_results.append(unwrapped)
        slower = wrap_comparison(
            "Nested Class Instancing:", wrapped, unwrapped
            )
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHOLD)

    def test_z_time_benchmark_results(self) -> None:
        slower = wrap_comparison("Overall:", self.wrapped, self.unwrapped)
        self.assertLess(slower, BENCHMARK_ASSERTION_THRESHOLD)

    @property
    def wrapped(self) -> float:
        return sum(self.wrapped_results) / len(self.wrapped_results)

    @property
    def unwrapped(self) -> float:
        return sum(self.unwrapped_results) / len(self.unwrapped_results)


if __name__ == "__main__":
    main()
