# instancemethod

Sections:

- [Purpose](#purpose)
- [Contents](#contents)
- [Installation](#installation)
- [Usage](#usage)
    - [Declaration](#declaration)
    - [Valid Usage](#valid-usage)
    - [Invalid Usage](#invalid-usage)
- [Issues/Limitations](#issueslimitations)
- [Testing](#testing)
- [Performance](#performance)
    - [Current Stats](#current-stats)
    - [Bottlenecks](#bottlenecks)

## Purpose

This package containing code and its example usage for restricting
method calls to instances of the class or subclass that contains the
method. Support has been added for nesting classes as attributes. 

## Contents

This package contains one module written in pure Python (3.5 or newer)
with the following code blocks:

- `instancemethod`: Higher order function for wrapping methods
- `NotAnInstanceError`: Error raised when validation fails

## Installation

This package is distributed to PyPi, and can be installed with either
of the following commands:

- `pip install instancemethod`
- `pip3 install instancemethod`

## Usage

Use the Python decorator (`@`) symbol along with the `instancemethod`
function to wrap a method and designate it as an instance method.

### Declaration

    class Foo:
        def __init__():
            ...
    
        @instancemethod
        def bar():
            ...

### Valid Usage

    foo = Foo()
    bar = foo.bar()

### Invalid Usage

    bar = Foo.bar()

Returns

    NotAnInstanceError:
    ...

## Issues/Limitations

There are currently no known stability or performance issues, so this 
package has been marked as:

***Production***

Previous [bottlenecks](#bottlenecks), a 
[deep-dive](#bottleneck-deep-dive) into their causes, and the 
explanation of their [solution](#bottleneck-solution) are located in 
the [Bottlenecks](#bottlenecks) portion of the 
[Performance](#performance) section.

## Testing

The following test cases are currently implemented:

- Decorator allows the following valid cases:
    - Calling method from an instance of a class
        - Foo().bar()
    - Calling method from an instance of a subclass
        - SubFoo().bar()
    - Calling method from an instance of a class in a nested hierarchy
        - Foo.Bar().foo()
- Decorator blocks all other cases:
    - Calling method without an instance of any above mentioned cases
        - Fuzzing implemented using instances of all built-in types
        and non-inheriting classes

## Performance

Performance testing is implemented for all valid test cases against a
control method. The control method is 
decorated with a `null_decorator` decorator that adds no functionality. 
This is compared to the `instancemethod` decorator; 1 Million 
function calls are made for each.

### Current Stats

The `instancemethod` decorator is currently:
1.64
times slower than `null_decorator` over the course of 1 Million calls.

Average Nanoseconds per Call:

- `instancemethod`: 139.2
- `null_decorator`: 85.0

***No*** appreciable difference has been found between the valid test
cases.

### Bottlenecks

Previous versions contained three main bottlenecks that hindered 
performance significantly (50x slower than `null_decorator`):

- The usage of the `inspect`.`getmodule` function
- The usage of the `inspect`.`getmembers` function
- The ownership attribute loop

### Bottleneck Deep-Dive

The `inspect` module and its `getmodule` and `getmembers` functions
are necessary for determining the class that has direct ownership of
the wrapped method. In previous versions, both the `getmodule` and 
`getmembers` functions were used in the wrapper function declared 
inside the higher order decorator.

Although marginal (5%) performance benefits were found by hoisting the 
`getmodule` up to the scope of the decorator function, by shifting the 
computation burden to declaration time as opposed to call time, the 
`getmembers` function was unable to be hoisted due to the changing 
state of a module at load time versus call time. Some performance was
reclaimed by the use of a lambda filtering predicate, but much was 
left to be desired.

Along with the `inspect` module functions, the "ownership attribute"
loop was another potential bottleneck. Since the only obvious way to
ascertain the class was through the method's fully qualified name,
accessing nested classes to reach down towards the method's direct
owner needed to be done using string attribute searches. Although the
loop is not too computationally intensive, this could be a bottleneck
for deeply nested or inherited class structures.

### Bottleneck Solution

The current solution in place was to extract the declaration and 
computation of these bottlenecks to a separate function in the 
package's local scope, as opposed to the decorator's scope, and 
enabling LRU caching from the `functools` module. 

For those unfamiliar, the lru_cache function, when used as a 
decorator, creates a memory-optimized call-result caching solution
that exchanges the full computation requirements of a function call
for a dictionary lookup of the result.

Since the penalty for a first-time call is 
~4 Microseconds, the caching of the results on a per-method basis 
provides a performance increase of 3,000%. This is because the 
dictionary lookup has a time complexity of, on average, O(1) that
results in ~125 Nanosecond follow-up calls.

## Author

Braden Toone is the sole author and maintainer of this code, and can
be contacted via email at braden@toonetown.com

## License

This package is licensed under the OSI Approved MIT License for free
commercial and personal use as stated in the LICENSE file.
