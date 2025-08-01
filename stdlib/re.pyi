import enum
import sre_compile
import sre_constants
import sys
from _typeshed import MaybeNone, ReadableBuffer
from collections.abc import Callable, Iterator, Mapping
from types import GenericAlias
from typing import Any, AnyStr, Final, Generic, Literal, TypeVar, final, overload
from typing_extensions import TypeAlias

__all__ = [
    "match",
    "fullmatch",
    "search",
    "sub",
    "subn",
    "split",
    "findall",
    "finditer",
    "compile",
    "purge",
    "escape",
    "error",
    "A",
    "I",
    "L",
    "M",
    "S",
    "X",
    "U",
    "ASCII",
    "IGNORECASE",
    "LOCALE",
    "MULTILINE",
    "DOTALL",
    "VERBOSE",
    "UNICODE",
    "Match",
    "Pattern",
]
if sys.version_info < (3, 13):
    __all__ += ["template"]

if sys.version_info >= (3, 11):
    __all__ += ["NOFLAG", "RegexFlag"]

if sys.version_info >= (3, 13):
    __all__ += ["PatternError"]

    PatternError = sre_constants.error

_T = TypeVar("_T")

# The implementation defines this in re._constants (version_info >= 3, 11) or
# sre_constants. Typeshed has it here because its __module__ attribute is set to "re".
class error(Exception):
    msg: str
    pattern: str | bytes | None
    pos: int | None
    lineno: int
    colno: int
    def __init__(self, msg: str, pattern: str | bytes | None = None, pos: int | None = None) -> None: ...

@final
class Match(Generic[AnyStr]):
    @property
    def pos(self) -> int: ...
    @property
    def endpos(self) -> int: ...
    @property
    def lastindex(self) -> int | None: ...
    @property
    def lastgroup(self) -> str | None: ...
    @property
    def string(self) -> AnyStr: ...

    # The regular expression object whose match() or search() method produced
    # this match instance.
    @property
    def re(self) -> Pattern[AnyStr]: ...
    @overload
    def expand(self: Match[str], template: str) -> str: ...
    @overload
    def expand(self: Match[bytes], template: ReadableBuffer) -> bytes: ...
    @overload
    def expand(self, template: AnyStr) -> AnyStr: ...
    # group() returns "AnyStr" or "AnyStr | None", depending on the pattern.
    @overload
    def group(self, group: Literal[0] = 0, /) -> AnyStr: ...
    @overload
    def group(self, group: str | int, /) -> AnyStr | MaybeNone: ...
    @overload
    def group(self, group1: str | int, group2: str | int, /, *groups: str | int) -> tuple[AnyStr | MaybeNone, ...]: ...
    # Each item of groups()'s return tuple is either "AnyStr" or
    # "AnyStr | None", depending on the pattern.
    @overload
    def groups(self) -> tuple[AnyStr | MaybeNone, ...]: ...
    @overload
    def groups(self, default: _T) -> tuple[AnyStr | _T, ...]: ...
    # Each value in groupdict()'s return dict is either "AnyStr" or
    # "AnyStr | None", depending on the pattern.
    @overload
    def groupdict(self) -> dict[str, AnyStr | MaybeNone]: ...
    @overload
    def groupdict(self, default: _T) -> dict[str, AnyStr | _T]: ...
    def start(self, group: int | str = 0, /) -> int: ...
    def end(self, group: int | str = 0, /) -> int: ...
    def span(self, group: int | str = 0, /) -> tuple[int, int]: ...
    @property
    def regs(self) -> tuple[tuple[int, int], ...]: ...  # undocumented
    # __getitem__() returns "AnyStr" or "AnyStr | None", depending on the pattern.
    @overload
    def __getitem__(self, key: Literal[0], /) -> AnyStr: ...
    @overload
    def __getitem__(self, key: int | str, /) -> AnyStr | MaybeNone: ...
    def __copy__(self) -> Match[AnyStr]: ...
    def __deepcopy__(self, memo: Any, /) -> Match[AnyStr]: ...
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...

@final
class Pattern(Generic[AnyStr]):
    @property
    def flags(self) -> int: ...
    @property
    def groupindex(self) -> Mapping[str, int]: ...
    @property
    def groups(self) -> int: ...
    @property
    def pattern(self) -> AnyStr: ...
    @overload
    def search(self: Pattern[str], string: str, pos: int = 0, endpos: int = sys.maxsize) -> Match[str] | None: ...
    @overload
    def search(self: Pattern[bytes], string: ReadableBuffer, pos: int = 0, endpos: int = sys.maxsize) -> Match[bytes] | None: ...
    @overload
    def search(self, string: AnyStr, pos: int = 0, endpos: int = sys.maxsize) -> Match[AnyStr] | None: ...
    @overload
    def match(self: Pattern[str], string: str, pos: int = 0, endpos: int = sys.maxsize) -> Match[str] | None: ...
    @overload
    def match(self: Pattern[bytes], string: ReadableBuffer, pos: int = 0, endpos: int = sys.maxsize) -> Match[bytes] | None: ...
    @overload
    def match(self, string: AnyStr, pos: int = 0, endpos: int = sys.maxsize) -> Match[AnyStr] | None: ...
    @overload
    def fullmatch(self: Pattern[str], string: str, pos: int = 0, endpos: int = sys.maxsize) -> Match[str] | None: ...
    @overload
    def fullmatch(
        self: Pattern[bytes], string: ReadableBuffer, pos: int = 0, endpos: int = sys.maxsize
    ) -> Match[bytes] | None: ...
    @overload
    def fullmatch(self, string: AnyStr, pos: int = 0, endpos: int = sys.maxsize) -> Match[AnyStr] | None: ...
    @overload
    def split(self: Pattern[str], string: str, maxsplit: int = 0) -> list[str | MaybeNone]: ...
    @overload
    def split(self: Pattern[bytes], string: ReadableBuffer, maxsplit: int = 0) -> list[bytes | MaybeNone]: ...
    @overload
    def split(self, string: AnyStr, maxsplit: int = 0) -> list[AnyStr | MaybeNone]: ...
    # return type depends on the number of groups in the pattern
    @overload
    def findall(self: Pattern[str], string: str, pos: int = 0, endpos: int = sys.maxsize) -> list[Any]: ...
    @overload
    def findall(self: Pattern[bytes], string: ReadableBuffer, pos: int = 0, endpos: int = sys.maxsize) -> list[Any]: ...
    @overload
    def findall(self, string: AnyStr, pos: int = 0, endpos: int = sys.maxsize) -> list[AnyStr]: ...
    @overload
    def finditer(self: Pattern[str], string: str, pos: int = 0, endpos: int = sys.maxsize) -> Iterator[Match[str]]: ...
    @overload
    def finditer(
        self: Pattern[bytes], string: ReadableBuffer, pos: int = 0, endpos: int = sys.maxsize
    ) -> Iterator[Match[bytes]]: ...
    @overload
    def finditer(self, string: AnyStr, pos: int = 0, endpos: int = sys.maxsize) -> Iterator[Match[AnyStr]]: ...
    @overload
    def sub(self: Pattern[str], repl: str | Callable[[Match[str]], str], string: str, count: int = 0) -> str: ...
    @overload
    def sub(
        self: Pattern[bytes],
        repl: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
        string: ReadableBuffer,
        count: int = 0,
    ) -> bytes: ...
    @overload
    def sub(self, repl: AnyStr | Callable[[Match[AnyStr]], AnyStr], string: AnyStr, count: int = 0) -> AnyStr: ...
    @overload
    def subn(self: Pattern[str], repl: str | Callable[[Match[str]], str], string: str, count: int = 0) -> tuple[str, int]: ...
    @overload
    def subn(
        self: Pattern[bytes],
        repl: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
        string: ReadableBuffer,
        count: int = 0,
    ) -> tuple[bytes, int]: ...
    @overload
    def subn(self, repl: AnyStr | Callable[[Match[AnyStr]], AnyStr], string: AnyStr, count: int = 0) -> tuple[AnyStr, int]: ...
    def __copy__(self) -> Pattern[AnyStr]: ...
    def __deepcopy__(self, memo: Any, /) -> Pattern[AnyStr]: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __hash__(self) -> int: ...
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...

# ----- re variables and constants -----

class RegexFlag(enum.IntFlag):
    A = sre_compile.SRE_FLAG_ASCII
    ASCII = A
    DEBUG = sre_compile.SRE_FLAG_DEBUG
    I = sre_compile.SRE_FLAG_IGNORECASE
    IGNORECASE = I
    L = sre_compile.SRE_FLAG_LOCALE
    LOCALE = L
    M = sre_compile.SRE_FLAG_MULTILINE
    MULTILINE = M
    S = sre_compile.SRE_FLAG_DOTALL
    DOTALL = S
    X = sre_compile.SRE_FLAG_VERBOSE
    VERBOSE = X
    U = sre_compile.SRE_FLAG_UNICODE
    UNICODE = U
    if sys.version_info < (3, 13):
        T = sre_compile.SRE_FLAG_TEMPLATE
        TEMPLATE = T
    if sys.version_info >= (3, 11):
        NOFLAG = 0

A: Final = RegexFlag.A
ASCII: Final = RegexFlag.ASCII
DEBUG: Final = RegexFlag.DEBUG
I: Final = RegexFlag.I
IGNORECASE: Final = RegexFlag.IGNORECASE
L: Final = RegexFlag.L
LOCALE: Final = RegexFlag.LOCALE
M: Final = RegexFlag.M
MULTILINE: Final = RegexFlag.MULTILINE
S: Final = RegexFlag.S
DOTALL: Final = RegexFlag.DOTALL
X: Final = RegexFlag.X
VERBOSE: Final = RegexFlag.VERBOSE
U: Final = RegexFlag.U
UNICODE: Final = RegexFlag.UNICODE
if sys.version_info < (3, 13):
    T: Final = RegexFlag.T
    TEMPLATE: Final = RegexFlag.TEMPLATE
if sys.version_info >= (3, 11):
    NOFLAG: Final = RegexFlag.NOFLAG
_FlagsType: TypeAlias = int | RegexFlag

# Type-wise the compile() overloads are unnecessary, they could also be modeled using
# unions in the parameter types. However mypy has a bug regarding TypeVar
# constraints (https://github.com/python/mypy/issues/11880),
# which limits us here because AnyStr is a constrained TypeVar.

# pattern arguments do *not* accept arbitrary buffers such as bytearray,
# because the pattern must be hashable.
@overload
def compile(pattern: AnyStr, flags: _FlagsType = 0) -> Pattern[AnyStr]: ...
@overload
def compile(pattern: Pattern[AnyStr], flags: _FlagsType = 0) -> Pattern[AnyStr]: ...
@overload
def search(pattern: str | Pattern[str], string: str, flags: _FlagsType = 0) -> Match[str] | None: ...
@overload
def search(pattern: bytes | Pattern[bytes], string: ReadableBuffer, flags: _FlagsType = 0) -> Match[bytes] | None: ...
@overload
def match(pattern: str | Pattern[str], string: str, flags: _FlagsType = 0) -> Match[str] | None: ...
@overload
def match(pattern: bytes | Pattern[bytes], string: ReadableBuffer, flags: _FlagsType = 0) -> Match[bytes] | None: ...
@overload
def fullmatch(pattern: str | Pattern[str], string: str, flags: _FlagsType = 0) -> Match[str] | None: ...
@overload
def fullmatch(pattern: bytes | Pattern[bytes], string: ReadableBuffer, flags: _FlagsType = 0) -> Match[bytes] | None: ...
@overload
def split(pattern: str | Pattern[str], string: str, maxsplit: int = 0, flags: _FlagsType = 0) -> list[str | MaybeNone]: ...
@overload
def split(
    pattern: bytes | Pattern[bytes], string: ReadableBuffer, maxsplit: int = 0, flags: _FlagsType = 0
) -> list[bytes | MaybeNone]: ...
@overload
def findall(pattern: str | Pattern[str], string: str, flags: _FlagsType = 0) -> list[Any]: ...
@overload
def findall(pattern: bytes | Pattern[bytes], string: ReadableBuffer, flags: _FlagsType = 0) -> list[Any]: ...
@overload
def finditer(pattern: str | Pattern[str], string: str, flags: _FlagsType = 0) -> Iterator[Match[str]]: ...
@overload
def finditer(pattern: bytes | Pattern[bytes], string: ReadableBuffer, flags: _FlagsType = 0) -> Iterator[Match[bytes]]: ...
@overload
def sub(
    pattern: str | Pattern[str], repl: str | Callable[[Match[str]], str], string: str, count: int = 0, flags: _FlagsType = 0
) -> str: ...
@overload
def sub(
    pattern: bytes | Pattern[bytes],
    repl: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
    string: ReadableBuffer,
    count: int = 0,
    flags: _FlagsType = 0,
) -> bytes: ...
@overload
def subn(
    pattern: str | Pattern[str], repl: str | Callable[[Match[str]], str], string: str, count: int = 0, flags: _FlagsType = 0
) -> tuple[str, int]: ...
@overload
def subn(
    pattern: bytes | Pattern[bytes],
    repl: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
    string: ReadableBuffer,
    count: int = 0,
    flags: _FlagsType = 0,
) -> tuple[bytes, int]: ...
def escape(pattern: AnyStr) -> AnyStr: ...
def purge() -> None: ...

if sys.version_info < (3, 13):
    def template(pattern: AnyStr | Pattern[AnyStr], flags: _FlagsType = 0) -> Pattern[AnyStr]: ...
