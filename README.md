# instancemethod

## Purpose

This package containing code and its example usage for restricting
method calls to instances of the class or subclass that contains the
method.

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

## Author

Braden Toone is the sole author and maintainer of this code, and can
be contacted via email at braden@toonetown.com

## License

This package is licensed under the OSI Approved MIT License.