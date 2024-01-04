# instancemethod

Sections:

- [Purpose](#purpose)
- [Contents](#contents)
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

There are currently no known stabilitiy issues, so this package has 
been marked as:

***Production***

There are some known performance bottlenecks, with specifics covered
in the [Bottlenecks](#bottlenecks) portion of the 
[Performance](#performance) section

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
46
times slower than `null_decorator` over the course of 1 Million calls.

Average Microseconds per Call:

- `instancemethod`: 3.85
- `null_decorator`: 0.08

***No*** appreciable difference has been found between the valid test
cases.

### Bottlenecks

There are two main bottlenecks that have been found:

- The usage of the `inspect` module
- The ownership attribute loop

The `inspect` module is used to get module and members that declared 
the function. This module is needed, as the package does not have 
adequate scope to use the `__class__` reference. Although the 
`getmodule` method can, and has, been hoisted to the highest order
function to place move the computation to the time of declaration as
opposed to call time, the `getmembers` method remains one order lower.

The `getmembers` method runs based on the state of a given module,
with a predicate implemented for faster elimination of invalid
potential method owners. If this method is called at declaration time,
it will frequently return no valid members. There is not a solution
obvious at this time.

Although the loop is not too computationally intensive, this is a
potential bottleneck for deeply nested or inherited class structures.
Some research has been done into object dictionary conversions with 
string indexing, but it has not yielded any appreciable benefit.

## Author

Braden Toone is the sole author and maintainer of this code, and can
be contacted via email at braden@toonetown.com

## License

This package is licensed under the OSI Approved MIT License for free
commercial and personal use as stated in the LICENSE file.
