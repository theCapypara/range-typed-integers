from itertools import chain
from typing import Optional, NewType, Annotated

from range_typed_integers import get_range, u8, ValueRange, check_int, u8_checked, IntegerBoundError


def test_get_range():
    assert get_range(int) is None
    assert get_range(None) is None
    assert get_range("abc") is None
    assert get_range(NewType("?", str)) is None
    assert ValueRange(min=0, max=255) == get_range(u8)
    assert ValueRange(min=0, max=255) == get_range(Optional[u8])
    assert ValueRange(min=0, max=255) == get_range(NewType('u8', Annotated[int, ValueRange(0, 255)]))
    assert ValueRange(min=0, max=123) == get_range(Annotated[int, ValueRange(0, 123)])
    assert ValueRange(min=0, max=456) == get_range(Optional[NewType('u8', Annotated[int, ValueRange(0, 456)])])


def test_check_int():
    class AnnotatedClass:
        a: int
        b: u8
        c: Optional[u8]
        d: NewType('u8', Annotated[int, ValueRange(0, 255)])
        e: Annotated[int, ValueRange(0, 255)]
        f: Optional[NewType('u8', Annotated[int, ValueRange(0, 255)])]

    for i in range(0, 256):
        assert check_int(int, i)
        assert check_int(u8, i)
        assert check_int(Optional[u8], i)
        assert check_int(NewType('u8', Annotated[int, ValueRange(0, 255)]), i)
        assert check_int(Annotated[int, ValueRange(0, 255)], i)
        assert check_int(Optional[NewType('u8', Annotated[int, ValueRange(0, 255)])], i)

        assert check_int((AnnotatedClass, 'a'), i)
        assert check_int((AnnotatedClass, 'b'), i)
        assert check_int((AnnotatedClass, 'c'), i)
        assert check_int((AnnotatedClass, 'd'), i)
        assert check_int((AnnotatedClass, 'e'), i)
        assert check_int((AnnotatedClass, 'f'), i)

    for i in chain(range(-20, 0), range(256, 512)):
        assert check_int(int, i)
        assert not check_int(u8, i)
        assert not check_int(Optional[u8], i)
        assert not check_int(NewType('u8', Annotated[int, ValueRange(0, 255)]), i)
        assert not check_int(Annotated[int, ValueRange(0, 255)], i)
        assert not check_int(Optional[NewType('u8', Annotated[int, ValueRange(0, 255)])], i)

        assert check_int((AnnotatedClass, 'a'), i)
        assert not check_int((AnnotatedClass, 'b'), i)
        assert not check_int((AnnotatedClass, 'c'), i)
        assert not check_int((AnnotatedClass, 'd'), i)
        assert not check_int((AnnotatedClass, 'e'), i)
        assert not check_int((AnnotatedClass, 'f'), i)

    assert check_int(Annotated[int, ValueRange(0, 12)], 3)
    assert not check_int(Annotated[int, ValueRange(0, 12)], 50)

    assert check_int(str, 3)
    assert check_int(str, "3")
    try:
        check_int(int, "3")
        assert check_int, "check_int must fail with (int, '3')."
    except ValueError:
        pass


def test_u8_checked():
    u8_checked(0)
    u8_checked(12)
    u8_checked(123)
    try:
        u8_checked(-1)
        assert False, "u8_checked must fail with -1."
    except IntegerBoundError:
        pass
    try:
        u8_checked(256)
        assert False, "u8_checked must fail with 256."
    except IntegerBoundError:
        pass
