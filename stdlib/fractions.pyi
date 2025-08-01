import sys
from collections.abc import Callable
from decimal import Decimal
from numbers import Rational, Real
from typing import Any, Literal, Protocol, SupportsIndex, overload, type_check_only
from typing_extensions import Self, TypeAlias

_ComparableNum: TypeAlias = int | float | Decimal | Real

__all__ = ["Fraction"]

@type_check_only
class _ConvertibleToIntegerRatio(Protocol):
    def as_integer_ratio(self) -> tuple[int | Rational, int | Rational]: ...

class Fraction(Rational):
    @overload
    def __new__(cls, numerator: int | Rational = 0, denominator: int | Rational | None = None) -> Self: ...
    @overload
    def __new__(cls, numerator: float | Decimal | str) -> Self: ...

    if sys.version_info >= (3, 14):
        @overload
        def __new__(cls, numerator: _ConvertibleToIntegerRatio) -> Self: ...

    @classmethod
    def from_float(cls, f: float) -> Self: ...
    @classmethod
    def from_decimal(cls, dec: Decimal) -> Self: ...
    def limit_denominator(self, max_denominator: int = 1000000) -> Fraction: ...
    def as_integer_ratio(self) -> tuple[int, int]: ...
    if sys.version_info >= (3, 12):
        def is_integer(self) -> bool: ...

    @property
    def numerator(a) -> int: ...
    @property
    def denominator(a) -> int: ...
    @overload
    def __add__(a, b: int | Fraction) -> Fraction: ...
    @overload
    def __add__(a, b: float) -> float: ...
    @overload
    def __add__(a, b: complex) -> complex: ...
    @overload
    def __radd__(b, a: int | Fraction) -> Fraction: ...
    @overload
    def __radd__(b, a: float) -> float: ...
    @overload
    def __radd__(b, a: complex) -> complex: ...
    @overload
    def __sub__(a, b: int | Fraction) -> Fraction: ...
    @overload
    def __sub__(a, b: float) -> float: ...
    @overload
    def __sub__(a, b: complex) -> complex: ...
    @overload
    def __rsub__(b, a: int | Fraction) -> Fraction: ...
    @overload
    def __rsub__(b, a: float) -> float: ...
    @overload
    def __rsub__(b, a: complex) -> complex: ...
    @overload
    def __mul__(a, b: int | Fraction) -> Fraction: ...
    @overload
    def __mul__(a, b: float) -> float: ...
    @overload
    def __mul__(a, b: complex) -> complex: ...
    @overload
    def __rmul__(b, a: int | Fraction) -> Fraction: ...
    @overload
    def __rmul__(b, a: float) -> float: ...
    @overload
    def __rmul__(b, a: complex) -> complex: ...
    @overload
    def __truediv__(a, b: int | Fraction) -> Fraction: ...
    @overload
    def __truediv__(a, b: float) -> float: ...
    @overload
    def __truediv__(a, b: complex) -> complex: ...
    @overload
    def __rtruediv__(b, a: int | Fraction) -> Fraction: ...
    @overload
    def __rtruediv__(b, a: float) -> float: ...
    @overload
    def __rtruediv__(b, a: complex) -> complex: ...
    @overload
    def __floordiv__(a, b: int | Fraction) -> int: ...
    @overload
    def __floordiv__(a, b: float) -> float: ...
    @overload
    def __rfloordiv__(b, a: int | Fraction) -> int: ...
    @overload
    def __rfloordiv__(b, a: float) -> float: ...
    @overload
    def __mod__(a, b: int | Fraction) -> Fraction: ...
    @overload
    def __mod__(a, b: float) -> float: ...
    @overload
    def __rmod__(b, a: int | Fraction) -> Fraction: ...
    @overload
    def __rmod__(b, a: float) -> float: ...
    @overload
    def __divmod__(a, b: int | Fraction) -> tuple[int, Fraction]: ...
    @overload
    def __divmod__(a, b: float) -> tuple[float, Fraction]: ...
    @overload
    def __rdivmod__(a, b: int | Fraction) -> tuple[int, Fraction]: ...
    @overload
    def __rdivmod__(a, b: float) -> tuple[float, Fraction]: ...
    if sys.version_info >= (3, 14):
        @overload
        def __pow__(a, b: int, modulo: None = None) -> Fraction: ...
        @overload
        def __pow__(a, b: float | Fraction, modulo: None = None) -> float: ...
        @overload
        def __pow__(a, b: complex, modulo: None = None) -> complex: ...
    else:
        @overload
        def __pow__(a, b: int) -> Fraction: ...
        @overload
        def __pow__(a, b: float | Fraction) -> float: ...
        @overload
        def __pow__(a, b: complex) -> complex: ...
    if sys.version_info >= (3, 14):
        @overload
        def __rpow__(b, a: float | Fraction, modulo: None = None) -> float: ...
        @overload
        def __rpow__(b, a: complex, modulo: None = None) -> complex: ...
    else:
        @overload
        def __rpow__(b, a: float | Fraction) -> float: ...
        @overload
        def __rpow__(b, a: complex) -> complex: ...

    def __pos__(a) -> Fraction: ...
    def __neg__(a) -> Fraction: ...
    def __abs__(a) -> Fraction: ...
    def __trunc__(a) -> int: ...
    def __floor__(a) -> int: ...
    def __ceil__(a) -> int: ...
    @overload
    def __round__(self, ndigits: None = None) -> int: ...
    @overload
    def __round__(self, ndigits: int) -> Fraction: ...
    def __hash__(self) -> int: ...  # type: ignore[override]
    def __eq__(a, b: object) -> bool: ...
    def __lt__(a, b: _ComparableNum) -> bool: ...
    def __gt__(a, b: _ComparableNum) -> bool: ...
    def __le__(a, b: _ComparableNum) -> bool: ...
    def __ge__(a, b: _ComparableNum) -> bool: ...
    def __bool__(a) -> bool: ...
    def __copy__(self) -> Self: ...
    def __deepcopy__(self, memo: Any) -> Self: ...
    if sys.version_info >= (3, 11):
        def __int__(a, _index: Callable[[SupportsIndex], int] = ...) -> int: ...
    # Not actually defined within fractions.py, but provides more useful
    # overrides
    @property
    def real(self) -> Fraction: ...
    @property
    def imag(self) -> Literal[0]: ...
    def conjugate(self) -> Fraction: ...
    if sys.version_info >= (3, 14):
        @classmethod
        def from_number(cls, number: float | Rational | _ConvertibleToIntegerRatio) -> Self: ...
