import sys
from abc import abstractmethod
from time import struct_time
from typing import ClassVar, Final, NoReturn, SupportsIndex, final, overload, type_check_only
from typing_extensions import CapsuleType, Self, TypeAlias, deprecated

if sys.version_info >= (3, 11):
    __all__ = ("date", "datetime", "time", "timedelta", "timezone", "tzinfo", "MINYEAR", "MAXYEAR", "UTC")
else:
    __all__ = ("date", "datetime", "time", "timedelta", "timezone", "tzinfo", "MINYEAR", "MAXYEAR")

MINYEAR: Final = 1
MAXYEAR: Final = 9999

class tzinfo:
    @abstractmethod
    def tzname(self, dt: datetime | None, /) -> str | None: ...
    @abstractmethod
    def utcoffset(self, dt: datetime | None, /) -> timedelta | None: ...
    @abstractmethod
    def dst(self, dt: datetime | None, /) -> timedelta | None: ...
    def fromutc(self, dt: datetime, /) -> datetime: ...

# Alias required to avoid name conflicts with date(time).tzinfo.
_TzInfo: TypeAlias = tzinfo

@final
class timezone(tzinfo):
    utc: ClassVar[timezone]
    min: ClassVar[timezone]
    max: ClassVar[timezone]
    def __new__(cls, offset: timedelta, name: str = ...) -> Self: ...
    def tzname(self, dt: datetime | None, /) -> str: ...
    def utcoffset(self, dt: datetime | None, /) -> timedelta: ...
    def dst(self, dt: datetime | None, /) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, value: object, /) -> bool: ...

if sys.version_info >= (3, 11):
    UTC: timezone

# This class calls itself datetime.IsoCalendarDate. It's neither
# NamedTuple nor structseq.
@final
@type_check_only
class _IsoCalendarDate(tuple[int, int, int]):
    @property
    def year(self) -> int: ...
    @property
    def week(self) -> int: ...
    @property
    def weekday(self) -> int: ...

class date:
    min: ClassVar[date]
    max: ClassVar[date]
    resolution: ClassVar[timedelta]
    def __new__(cls, year: SupportsIndex, month: SupportsIndex, day: SupportsIndex) -> Self: ...
    @classmethod
    def fromtimestamp(cls, timestamp: float, /) -> Self: ...
    @classmethod
    def today(cls) -> Self: ...
    @classmethod
    def fromordinal(cls, n: int, /) -> Self: ...
    @classmethod
    def fromisoformat(cls, date_string: str, /) -> Self: ...
    @classmethod
    def fromisocalendar(cls, year: int, week: int, day: int) -> Self: ...
    @property
    def year(self) -> int: ...
    @property
    def month(self) -> int: ...
    @property
    def day(self) -> int: ...
    def ctime(self) -> str: ...

    if sys.version_info >= (3, 14):
        @classmethod
        def strptime(cls, date_string: str, format: str, /) -> Self: ...

    # On <3.12, the name of the parameter in the pure-Python implementation
    # didn't match the name in the C implementation,
    # meaning it is only *safe* to pass it as a keyword argument on 3.12+
    if sys.version_info >= (3, 12):
        def strftime(self, format: str) -> str: ...
    else:
        def strftime(self, format: str, /) -> str: ...

    def __format__(self, fmt: str, /) -> str: ...
    def isoformat(self) -> str: ...
    def timetuple(self) -> struct_time: ...
    def toordinal(self) -> int: ...
    if sys.version_info >= (3, 13):
        def __replace__(self, /, *, year: SupportsIndex = ..., month: SupportsIndex = ..., day: SupportsIndex = ...) -> Self: ...

    def replace(self, year: SupportsIndex = ..., month: SupportsIndex = ..., day: SupportsIndex = ...) -> Self: ...
    def __le__(self, value: date, /) -> bool: ...
    def __lt__(self, value: date, /) -> bool: ...
    def __ge__(self, value: date, /) -> bool: ...
    def __gt__(self, value: date, /) -> bool: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __add__(self, value: timedelta, /) -> Self: ...
    def __radd__(self, value: timedelta, /) -> Self: ...
    @overload
    def __sub__(self, value: datetime, /) -> NoReturn: ...
    @overload
    def __sub__(self, value: Self, /) -> timedelta: ...
    @overload
    def __sub__(self, value: timedelta, /) -> Self: ...
    def __hash__(self) -> int: ...
    def weekday(self) -> int: ...
    def isoweekday(self) -> int: ...
    def isocalendar(self) -> _IsoCalendarDate: ...

class time:
    min: ClassVar[time]
    max: ClassVar[time]
    resolution: ClassVar[timedelta]
    def __new__(
        cls,
        hour: SupportsIndex = 0,
        minute: SupportsIndex = 0,
        second: SupportsIndex = 0,
        microsecond: SupportsIndex = 0,
        tzinfo: _TzInfo | None = None,
        *,
        fold: int = 0,
    ) -> Self: ...
    @property
    def hour(self) -> int: ...
    @property
    def minute(self) -> int: ...
    @property
    def second(self) -> int: ...
    @property
    def microsecond(self) -> int: ...
    @property
    def tzinfo(self) -> _TzInfo | None: ...
    @property
    def fold(self) -> int: ...
    def __le__(self, value: time, /) -> bool: ...
    def __lt__(self, value: time, /) -> bool: ...
    def __ge__(self, value: time, /) -> bool: ...
    def __gt__(self, value: time, /) -> bool: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __hash__(self) -> int: ...
    def isoformat(self, timespec: str = "auto") -> str: ...
    @classmethod
    def fromisoformat(cls, time_string: str, /) -> Self: ...

    if sys.version_info >= (3, 14):
        @classmethod
        def strptime(cls, date_string: str, format: str, /) -> Self: ...

    # On <3.12, the name of the parameter in the pure-Python implementation
    # didn't match the name in the C implementation,
    # meaning it is only *safe* to pass it as a keyword argument on 3.12+
    if sys.version_info >= (3, 12):
        def strftime(self, format: str) -> str: ...
    else:
        def strftime(self, format: str, /) -> str: ...

    def __format__(self, fmt: str, /) -> str: ...
    def utcoffset(self) -> timedelta | None: ...
    def tzname(self) -> str | None: ...
    def dst(self) -> timedelta | None: ...
    if sys.version_info >= (3, 13):
        def __replace__(
            self,
            /,
            *,
            hour: SupportsIndex = ...,
            minute: SupportsIndex = ...,
            second: SupportsIndex = ...,
            microsecond: SupportsIndex = ...,
            tzinfo: _TzInfo | None = ...,
            fold: int = ...,
        ) -> Self: ...

    def replace(
        self,
        hour: SupportsIndex = ...,
        minute: SupportsIndex = ...,
        second: SupportsIndex = ...,
        microsecond: SupportsIndex = ...,
        tzinfo: _TzInfo | None = ...,
        *,
        fold: int = ...,
    ) -> Self: ...

_Date: TypeAlias = date
_Time: TypeAlias = time

class timedelta:
    min: ClassVar[timedelta]
    max: ClassVar[timedelta]
    resolution: ClassVar[timedelta]
    def __new__(
        cls,
        days: float = 0,
        seconds: float = 0,
        microseconds: float = 0,
        milliseconds: float = 0,
        minutes: float = 0,
        hours: float = 0,
        weeks: float = 0,
    ) -> Self: ...
    @property
    def days(self) -> int: ...
    @property
    def seconds(self) -> int: ...
    @property
    def microseconds(self) -> int: ...
    def total_seconds(self) -> float: ...
    def __add__(self, value: timedelta, /) -> timedelta: ...
    def __radd__(self, value: timedelta, /) -> timedelta: ...
    def __sub__(self, value: timedelta, /) -> timedelta: ...
    def __rsub__(self, value: timedelta, /) -> timedelta: ...
    def __neg__(self) -> timedelta: ...
    def __pos__(self) -> timedelta: ...
    def __abs__(self) -> timedelta: ...
    def __mul__(self, value: float, /) -> timedelta: ...
    def __rmul__(self, value: float, /) -> timedelta: ...
    @overload
    def __floordiv__(self, value: timedelta, /) -> int: ...
    @overload
    def __floordiv__(self, value: int, /) -> timedelta: ...
    @overload
    def __truediv__(self, value: timedelta, /) -> float: ...
    @overload
    def __truediv__(self, value: float, /) -> timedelta: ...
    def __mod__(self, value: timedelta, /) -> timedelta: ...
    def __divmod__(self, value: timedelta, /) -> tuple[int, timedelta]: ...
    def __le__(self, value: timedelta, /) -> bool: ...
    def __lt__(self, value: timedelta, /) -> bool: ...
    def __ge__(self, value: timedelta, /) -> bool: ...
    def __gt__(self, value: timedelta, /) -> bool: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __bool__(self) -> bool: ...
    def __hash__(self) -> int: ...

class datetime(date):
    min: ClassVar[datetime]
    max: ClassVar[datetime]
    def __new__(
        cls,
        year: SupportsIndex,
        month: SupportsIndex,
        day: SupportsIndex,
        hour: SupportsIndex = 0,
        minute: SupportsIndex = 0,
        second: SupportsIndex = 0,
        microsecond: SupportsIndex = 0,
        tzinfo: _TzInfo | None = None,
        *,
        fold: int = 0,
    ) -> Self: ...
    @property
    def hour(self) -> int: ...
    @property
    def minute(self) -> int: ...
    @property
    def second(self) -> int: ...
    @property
    def microsecond(self) -> int: ...
    @property
    def tzinfo(self) -> _TzInfo | None: ...
    @property
    def fold(self) -> int: ...
    # On <3.12, the name of the first parameter in the pure-Python implementation
    # didn't match the name in the C implementation,
    # meaning it is only *safe* to pass it as a keyword argument on 3.12+
    if sys.version_info >= (3, 12):
        @classmethod
        def fromtimestamp(cls, timestamp: float, tz: _TzInfo | None = None) -> Self: ...
    else:
        @classmethod
        def fromtimestamp(cls, timestamp: float, /, tz: _TzInfo | None = None) -> Self: ...

    @classmethod
    @deprecated("Use timezone-aware objects to represent datetimes in UTC; e.g. by calling .fromtimestamp(datetime.timezone.utc)")
    def utcfromtimestamp(cls, t: float, /) -> Self: ...
    @classmethod
    def now(cls, tz: _TzInfo | None = None) -> Self: ...
    @classmethod
    @deprecated("Use timezone-aware objects to represent datetimes in UTC; e.g. by calling .now(datetime.timezone.utc)")
    def utcnow(cls) -> Self: ...
    @classmethod
    def combine(cls, date: _Date, time: _Time, tzinfo: _TzInfo | None = ...) -> Self: ...
    def timestamp(self) -> float: ...
    def utctimetuple(self) -> struct_time: ...
    def date(self) -> _Date: ...
    def time(self) -> _Time: ...
    def timetz(self) -> _Time: ...
    if sys.version_info >= (3, 13):
        def __replace__(
            self,
            /,
            *,
            year: SupportsIndex = ...,
            month: SupportsIndex = ...,
            day: SupportsIndex = ...,
            hour: SupportsIndex = ...,
            minute: SupportsIndex = ...,
            second: SupportsIndex = ...,
            microsecond: SupportsIndex = ...,
            tzinfo: _TzInfo | None = ...,
            fold: int = ...,
        ) -> Self: ...

    def replace(
        self,
        year: SupportsIndex = ...,
        month: SupportsIndex = ...,
        day: SupportsIndex = ...,
        hour: SupportsIndex = ...,
        minute: SupportsIndex = ...,
        second: SupportsIndex = ...,
        microsecond: SupportsIndex = ...,
        tzinfo: _TzInfo | None = ...,
        *,
        fold: int = ...,
    ) -> Self: ...
    def astimezone(self, tz: _TzInfo | None = None) -> Self: ...
    def isoformat(self, sep: str = "T", timespec: str = "auto") -> str: ...
    @classmethod
    def strptime(cls, date_string: str, format: str, /) -> Self: ...
    def utcoffset(self) -> timedelta | None: ...
    def tzname(self) -> str | None: ...
    def dst(self) -> timedelta | None: ...
    def __le__(self, value: datetime, /) -> bool: ...  # type: ignore[override]
    def __lt__(self, value: datetime, /) -> bool: ...  # type: ignore[override]
    def __ge__(self, value: datetime, /) -> bool: ...  # type: ignore[override]
    def __gt__(self, value: datetime, /) -> bool: ...  # type: ignore[override]
    def __eq__(self, value: object, /) -> bool: ...
    def __hash__(self) -> int: ...
    @overload  # type: ignore[override]
    def __sub__(self, value: Self, /) -> timedelta: ...
    @overload
    def __sub__(self, value: timedelta, /) -> Self: ...

datetime_CAPI: CapsuleType
