Range-Typed Integers
====================

This package provides integer types that have a specific range of valid values.

.. _mypy: https://mypy.readthedocs.io/

Usage
-----
The package provides some types (as `NewType`_) that represent their respective `Rust integer type`_:
``u8``, ``u16``, ``u32``, ``u64``, ``i8``, ``i16``, ``i32`` and ``i64``::

    from range_typed_integers import u8, i8

    # u8 is an unsigned 8-bit integer so its range is 0-255:
    a: u8 = 12  # valid
    a: u8 = -12  # invalid - The type checker should mark this as an error.
    a: u8 = 900  # invalid - The type checker should mark this as an error.

The types are defined as ``NewTypes`` of ``ValueRange`` annotated integers. This is also how
you can define your own custom ranged integer types. As an example this is literally how
``range_typed_integers.i8`` is defined::

    from typing import Annotated, NewType
    from range_typed_integers import ValueRange

    i8 = NewType('i8', Annotated[int, ValueRange(-128, 127)])

To cast values to typed integers, you can:

- use the NewType's constructor: ``i8(12)``
- Use the "checked constructors": ``i8_checked(12)``.
  These will raise a ``IntegerBoundError`` if the value is out of range (subclass of ``OverflowError``).
- use the `cast`_ function: ``cast(i8, 12)``

.. _Rust integer type: https://doc.rust-lang.org/book/ch03-02-data-types.html#integer-types
.. _NewType: https://docs.python.org/3/library/typing.html#newtype
.. _cast: https://docs.python.org/3/library/typing.html#typing.cast

Runtime checking
----------------
You can use the function ``check_int`` to check if an integer fits into any integer type.::

    >>> from range_typed_integers import check_int, u8
    >>>
    >>> class A
    ...     field: u8
    ...
    >>> # You can use this directly with a type.
    >>> check_int(u8, 0)
    True
    >>> check_int(u8, -1)
    False
    >>> # Or have the function look up the type annotations for an attribute on an object.
    >>> check_int((A, 'field'), 0)
    True
    >>> check_int((A, 'field'), 256)
    False
    >>> # You can also use this with non-ranged integers (will always return True).
    >>> check_int(int, 1234567)
    True
    >>> # Or even arbitrary types (will always return True and do no type validation).
    >>> check_int(str, 1234)
    True

For ease-of-use the types shipped with this package, also have "checked constructors" (eg. ``u8_checked``),
that will cast a value to their type and raise an ``IntegerBoundError`` if the value is out of range.

MyPy and Python Support
-----------------------
This is only truly supported in Python 3.9+, due to the lack of the ``Annotated`` type in earlier versions.

However 3.8 is also supported via ``typing_extensions``. Note however, that MyPy with Python 3.8 will not accept
``Annotated`` as a type to use with ``NewType``.
