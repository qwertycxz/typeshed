import sys
from _typeshed import StrPath
from py_compile import PycInvalidationMode
from typing import Any, Protocol, type_check_only

__all__ = ["compile_dir", "compile_file", "compile_path"]

@type_check_only
class _SupportsSearch(Protocol):
    def search(self, string: str, /) -> Any: ...

if sys.version_info >= (3, 10):
    def compile_dir(
        dir: StrPath,
        maxlevels: int | None = None,
        ddir: StrPath | None = None,
        force: bool = False,
        rx: _SupportsSearch | None = None,
        quiet: int = 0,
        legacy: bool = False,
        optimize: int = -1,
        workers: int = 1,
        invalidation_mode: PycInvalidationMode | None = None,
        *,
        stripdir: StrPath | None = None,
        prependdir: StrPath | None = None,
        limit_sl_dest: StrPath | None = None,
        hardlink_dupes: bool = False,
    ) -> bool: ...
    def compile_file(
        fullname: StrPath,
        ddir: StrPath | None = None,
        force: bool = False,
        rx: _SupportsSearch | None = None,
        quiet: int = 0,
        legacy: bool = False,
        optimize: int = -1,
        invalidation_mode: PycInvalidationMode | None = None,
        *,
        stripdir: StrPath | None = None,
        prependdir: StrPath | None = None,
        limit_sl_dest: StrPath | None = None,
        hardlink_dupes: bool = False,
    ) -> bool: ...

else:
    def compile_dir(
        dir: StrPath,
        maxlevels: int | None = None,
        ddir: StrPath | None = None,
        force: bool = False,
        rx: _SupportsSearch | None = None,
        quiet: int = 0,
        legacy: bool = False,
        optimize: int = -1,
        workers: int = 1,
        invalidation_mode: PycInvalidationMode | None = None,
        *,
        stripdir: str | None = None,  # https://bugs.python.org/issue40447
        prependdir: StrPath | None = None,
        limit_sl_dest: StrPath | None = None,
        hardlink_dupes: bool = False,
    ) -> bool: ...
    def compile_file(
        fullname: StrPath,
        ddir: StrPath | None = None,
        force: bool = False,
        rx: _SupportsSearch | None = None,
        quiet: int = 0,
        legacy: bool = False,
        optimize: int = -1,
        invalidation_mode: PycInvalidationMode | None = None,
        *,
        stripdir: str | None = None,  # https://bugs.python.org/issue40447
        prependdir: StrPath | None = None,
        limit_sl_dest: StrPath | None = None,
        hardlink_dupes: bool = False,
    ) -> bool: ...

def compile_path(
    skip_curdir: bool = ...,
    maxlevels: int = 0,
    force: bool = False,
    quiet: int = 0,
    legacy: bool = False,
    optimize: int = -1,
    invalidation_mode: PycInvalidationMode | None = None,
) -> bool: ...
