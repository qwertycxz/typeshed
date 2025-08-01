import sys
from _typeshed import SupportsWrite, sentinel
from collections.abc import Callable, Generator, Iterable, Sequence
from re import Pattern
from typing import IO, Any, ClassVar, Final, Generic, NoReturn, Protocol, TypeVar, overload, type_check_only
from typing_extensions import Self, TypeAlias, deprecated

__all__ = [
    "ArgumentParser",
    "ArgumentError",
    "ArgumentTypeError",
    "FileType",
    "HelpFormatter",
    "ArgumentDefaultsHelpFormatter",
    "RawDescriptionHelpFormatter",
    "RawTextHelpFormatter",
    "MetavarTypeHelpFormatter",
    "Namespace",
    "Action",
    "BooleanOptionalAction",
    "ONE_OR_MORE",
    "OPTIONAL",
    "PARSER",
    "REMAINDER",
    "SUPPRESS",
    "ZERO_OR_MORE",
]

_T = TypeVar("_T")
_ActionT = TypeVar("_ActionT", bound=Action)
_ArgumentParserT = TypeVar("_ArgumentParserT", bound=ArgumentParser)
_N = TypeVar("_N")
_ActionType: TypeAlias = Callable[[str], Any] | FileType | str

ONE_OR_MORE: Final = "+"
OPTIONAL: Final = "?"
PARSER: Final = "A..."
REMAINDER: Final = "..."
SUPPRESS: Final = "==SUPPRESS=="
ZERO_OR_MORE: Final = "*"
_UNRECOGNIZED_ARGS_ATTR: Final = "_unrecognized_args"  # undocumented

class ArgumentError(Exception):
    argument_name: str | None
    message: str
    def __init__(self, argument: Action | None, message: str) -> None: ...

# undocumented
class _AttributeHolder:
    def _get_kwargs(self) -> list[tuple[str, Any]]: ...
    def _get_args(self) -> list[Any]: ...

# undocumented
class _ActionsContainer:
    description: str | None
    prefix_chars: str
    argument_default: Any
    conflict_handler: str

    _registries: dict[str, dict[Any, Any]]
    _actions: list[Action]
    _option_string_actions: dict[str, Action]
    _action_groups: list[_ArgumentGroup]
    _mutually_exclusive_groups: list[_MutuallyExclusiveGroup]
    _defaults: dict[str, Any]
    _negative_number_matcher: Pattern[str]
    _has_negative_number_optionals: list[bool]
    def __init__(self, description: str | None, prefix_chars: str, argument_default: Any, conflict_handler: str) -> None: ...
    def register(self, registry_name: str, value: Any, object: Any) -> None: ...
    def _registry_get(self, registry_name: str, value: Any, default: Any = None) -> Any: ...
    def set_defaults(self, **kwargs: Any) -> None: ...
    def get_default(self, dest: str) -> Any: ...
    def add_argument(
        self,
        *name_or_flags: str,
        # str covers predefined actions ("store_true", "count", etc.)
        # and user registered actions via the `register` method.
        action: str | type[Action] = ...,
        # more precisely, Literal["?", "*", "+", "...", "A...", "==SUPPRESS=="],
        # but using this would make it hard to annotate callers that don't use a
        # literal argument and for subclasses to override this method.
        nargs: int | str | None = None,
        const: Any = ...,
        default: Any = ...,
        type: _ActionType = ...,
        choices: Iterable[_T] | None = ...,
        required: bool = ...,
        help: str | None = ...,
        metavar: str | tuple[str, ...] | None = ...,
        dest: str | None = ...,
        version: str = ...,
        **kwargs: Any,
    ) -> Action: ...
    def add_argument_group(
        self,
        title: str | None = None,
        description: str | None = None,
        *,
        prefix_chars: str = ...,
        argument_default: Any = ...,
        conflict_handler: str = ...,
    ) -> _ArgumentGroup: ...
    def add_mutually_exclusive_group(self, *, required: bool = False) -> _MutuallyExclusiveGroup: ...
    def _add_action(self, action: _ActionT) -> _ActionT: ...
    def _remove_action(self, action: Action) -> None: ...
    def _add_container_actions(self, container: _ActionsContainer) -> None: ...
    def _get_positional_kwargs(self, dest: str, **kwargs: Any) -> dict[str, Any]: ...
    def _get_optional_kwargs(self, *args: Any, **kwargs: Any) -> dict[str, Any]: ...
    def _pop_action_class(self, kwargs: Any, default: type[Action] | None = None) -> type[Action]: ...
    def _get_handler(self) -> Callable[[Action, Iterable[tuple[str, Action]]], Any]: ...
    def _check_conflict(self, action: Action) -> None: ...
    def _handle_conflict_error(self, action: Action, conflicting_actions: Iterable[tuple[str, Action]]) -> NoReturn: ...
    def _handle_conflict_resolve(self, action: Action, conflicting_actions: Iterable[tuple[str, Action]]) -> None: ...

@type_check_only
class _FormatterClass(Protocol):
    def __call__(self, *, prog: str) -> HelpFormatter: ...

class ArgumentParser(_AttributeHolder, _ActionsContainer):
    prog: str
    usage: str | None
    epilog: str | None
    formatter_class: _FormatterClass
    fromfile_prefix_chars: str | None
    add_help: bool
    allow_abbrev: bool
    exit_on_error: bool

    if sys.version_info >= (3, 14):
        suggest_on_error: bool
        color: bool

    # undocumented
    _positionals: _ArgumentGroup
    _optionals: _ArgumentGroup
    _subparsers: _ArgumentGroup | None

    # Note: the constructor arguments are also used in _SubParsersAction.add_parser.
    if sys.version_info >= (3, 14):
        def __init__(
            self,
            prog: str | None = None,
            usage: str | None = None,
            description: str | None = None,
            epilog: str | None = None,
            parents: Sequence[ArgumentParser] = [],
            formatter_class: _FormatterClass = ...,
            prefix_chars: str = "-",
            fromfile_prefix_chars: str | None = None,
            argument_default: Any = None,
            conflict_handler: str = "error",
            add_help: bool = True,
            allow_abbrev: bool = True,
            exit_on_error: bool = True,
            *,
            suggest_on_error: bool = False,
            color: bool = False,
        ) -> None: ...
    else:
        def __init__(
            self,
            prog: str | None = None,
            usage: str | None = None,
            description: str | None = None,
            epilog: str | None = None,
            parents: Sequence[ArgumentParser] = [],
            formatter_class: _FormatterClass = ...,
            prefix_chars: str = "-",
            fromfile_prefix_chars: str | None = None,
            argument_default: Any = None,
            conflict_handler: str = "error",
            add_help: bool = True,
            allow_abbrev: bool = True,
            exit_on_error: bool = True,
        ) -> None: ...

    @overload
    def parse_args(self, args: Sequence[str] | None = None, namespace: None = None) -> Namespace: ...
    @overload
    def parse_args(self, args: Sequence[str] | None, namespace: _N) -> _N: ...
    @overload
    def parse_args(self, *, namespace: _N) -> _N: ...
    @overload
    def add_subparsers(
        self: _ArgumentParserT,
        *,
        title: str = "subcommands",
        description: str | None = None,
        prog: str | None = None,
        action: type[Action] = ...,
        option_string: str = ...,
        dest: str | None = None,
        required: bool = False,
        help: str | None = None,
        metavar: str | None = None,
    ) -> _SubParsersAction[_ArgumentParserT]: ...
    @overload
    def add_subparsers(
        self,
        *,
        title: str = "subcommands",
        description: str | None = None,
        prog: str | None = None,
        parser_class: type[_ArgumentParserT],
        action: type[Action] = ...,
        option_string: str = ...,
        dest: str | None = None,
        required: bool = False,
        help: str | None = None,
        metavar: str | None = None,
    ) -> _SubParsersAction[_ArgumentParserT]: ...
    def print_usage(self, file: SupportsWrite[str] | None = None) -> None: ...
    def print_help(self, file: SupportsWrite[str] | None = None) -> None: ...
    def format_usage(self) -> str: ...
    def format_help(self) -> str: ...
    @overload
    def parse_known_args(self, args: Sequence[str] | None = None, namespace: None = None) -> tuple[Namespace, list[str]]: ...
    @overload
    def parse_known_args(self, args: Sequence[str] | None, namespace: _N) -> tuple[_N, list[str]]: ...
    @overload
    def parse_known_args(self, *, namespace: _N) -> tuple[_N, list[str]]: ...
    def convert_arg_line_to_args(self, arg_line: str) -> list[str]: ...
    def exit(self, status: int = 0, message: str | None = None) -> NoReturn: ...
    def error(self, message: str) -> NoReturn: ...
    @overload
    def parse_intermixed_args(self, args: Sequence[str] | None = None, namespace: None = None) -> Namespace: ...
    @overload
    def parse_intermixed_args(self, args: Sequence[str] | None, namespace: _N) -> _N: ...
    @overload
    def parse_intermixed_args(self, *, namespace: _N) -> _N: ...
    @overload
    def parse_known_intermixed_args(
        self, args: Sequence[str] | None = None, namespace: None = None
    ) -> tuple[Namespace, list[str]]: ...
    @overload
    def parse_known_intermixed_args(self, args: Sequence[str] | None, namespace: _N) -> tuple[_N, list[str]]: ...
    @overload
    def parse_known_intermixed_args(self, *, namespace: _N) -> tuple[_N, list[str]]: ...
    # undocumented
    def _get_optional_actions(self) -> list[Action]: ...
    def _get_positional_actions(self) -> list[Action]: ...
    if sys.version_info >= (3, 12):
        def _parse_known_args(
            self, arg_strings: list[str], namespace: Namespace, intermixed: bool
        ) -> tuple[Namespace, list[str]]: ...
    else:
        def _parse_known_args(self, arg_strings: list[str], namespace: Namespace) -> tuple[Namespace, list[str]]: ...

    def _read_args_from_files(self, arg_strings: list[str]) -> list[str]: ...
    def _match_argument(self, action: Action, arg_strings_pattern: str) -> int: ...
    def _match_arguments_partial(self, actions: Sequence[Action], arg_strings_pattern: str) -> list[int]: ...
    def _parse_optional(self, arg_string: str) -> tuple[Action | None, str, str | None] | None: ...
    def _get_option_tuples(self, option_string: str) -> list[tuple[Action, str, str | None]]: ...
    def _get_nargs_pattern(self, action: Action) -> str: ...
    def _get_values(self, action: Action, arg_strings: list[str]) -> Any: ...
    def _get_value(self, action: Action, arg_string: str) -> Any: ...
    def _check_value(self, action: Action, value: Any) -> None: ...
    def _get_formatter(self) -> HelpFormatter: ...
    def _print_message(self, message: str, file: SupportsWrite[str] | None = None) -> None: ...

class HelpFormatter:
    # undocumented
    _prog: str
    _indent_increment: int
    _max_help_position: int
    _width: int
    _current_indent: int
    _level: int
    _action_max_length: int
    _root_section: _Section
    _current_section: _Section
    _whitespace_matcher: Pattern[str]
    _long_break_matcher: Pattern[str]

    class _Section:
        formatter: HelpFormatter
        heading: str | None
        parent: Self | None
        items: list[tuple[Callable[..., str], Iterable[Any]]]
        def __init__(self, formatter: HelpFormatter, parent: Self | None, heading: str | None = None) -> None: ...
        def format_help(self) -> str: ...

    if sys.version_info >= (3, 14):
        def __init__(
            self, prog: str, indent_increment: int = 2, max_help_position: int = 24, width: int | None = None, color: bool = True
        ) -> None: ...
    else:
        def __init__(
            self, prog: str, indent_increment: int = 2, max_help_position: int = 24, width: int | None = None
        ) -> None: ...

    def _indent(self) -> None: ...
    def _dedent(self) -> None: ...
    def _add_item(self, func: Callable[..., str], args: Iterable[Any]) -> None: ...
    def start_section(self, heading: str | None) -> None: ...
    def end_section(self) -> None: ...
    def add_text(self, text: str | None) -> None: ...
    def add_usage(
        self, usage: str | None, actions: Iterable[Action], groups: Iterable[_MutuallyExclusiveGroup], prefix: str | None = None
    ) -> None: ...
    def add_argument(self, action: Action) -> None: ...
    def add_arguments(self, actions: Iterable[Action]) -> None: ...
    def format_help(self) -> str: ...
    def _join_parts(self, part_strings: Iterable[str]) -> str: ...
    def _format_usage(
        self, usage: str | None, actions: Iterable[Action], groups: Iterable[_MutuallyExclusiveGroup], prefix: str | None
    ) -> str: ...
    def _format_actions_usage(self, actions: Iterable[Action], groups: Iterable[_MutuallyExclusiveGroup]) -> str: ...
    def _format_text(self, text: str) -> str: ...
    def _format_action(self, action: Action) -> str: ...
    def _format_action_invocation(self, action: Action) -> str: ...
    def _metavar_formatter(self, action: Action, default_metavar: str) -> Callable[[int], tuple[str, ...]]: ...
    def _format_args(self, action: Action, default_metavar: str) -> str: ...
    def _expand_help(self, action: Action) -> str: ...
    def _iter_indented_subactions(self, action: Action) -> Generator[Action, None, None]: ...
    def _split_lines(self, text: str, width: int) -> list[str]: ...
    def _fill_text(self, text: str, width: int, indent: str) -> str: ...
    def _get_help_string(self, action: Action) -> str | None: ...
    def _get_default_metavar_for_optional(self, action: Action) -> str: ...
    def _get_default_metavar_for_positional(self, action: Action) -> str: ...

class RawDescriptionHelpFormatter(HelpFormatter): ...
class RawTextHelpFormatter(RawDescriptionHelpFormatter): ...
class ArgumentDefaultsHelpFormatter(HelpFormatter): ...
class MetavarTypeHelpFormatter(HelpFormatter): ...

class Action(_AttributeHolder):
    option_strings: Sequence[str]
    dest: str
    nargs: int | str | None
    const: Any
    default: Any
    type: _ActionType | None
    choices: Iterable[Any] | None
    required: bool
    help: str | None
    metavar: str | tuple[str, ...] | None
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            nargs: int | str | None = None,
            const: _T | None = None,
            default: _T | str | None = None,
            type: Callable[[str], _T] | FileType | None = None,
            choices: Iterable[_T] | None = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
            deprecated: bool = False,
        ) -> None: ...
    else:
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            nargs: int | str | None = None,
            const: _T | None = None,
            default: _T | str | None = None,
            type: Callable[[str], _T] | FileType | None = None,
            choices: Iterable[_T] | None = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
        ) -> None: ...

    def __call__(
        self, parser: ArgumentParser, namespace: Namespace, values: str | Sequence[Any] | None, option_string: str | None = None
    ) -> None: ...
    def format_usage(self) -> str: ...

if sys.version_info >= (3, 12):
    class BooleanOptionalAction(Action):
        if sys.version_info >= (3, 14):
            def __init__(
                self,
                option_strings: Sequence[str],
                dest: str,
                default: bool | None = None,
                required: bool = False,
                help: str | None = None,
                deprecated: bool = False,
            ) -> None: ...
        elif sys.version_info >= (3, 13):
            @overload
            def __init__(
                self,
                option_strings: Sequence[str],
                dest: str,
                default: bool | None = None,
                *,
                required: bool = False,
                help: str | None = None,
                deprecated: bool = False,
            ) -> None: ...
            @overload
            @deprecated("The `type`, `choices`, and `metavar` parameters are ignored and will be removed in Python 3.14.")
            def __init__(
                self,
                option_strings: Sequence[str],
                dest: str,
                default: _T | bool | None = None,
                type: Callable[[str], _T] | FileType | None = sentinel,
                choices: Iterable[_T] | None = sentinel,
                required: bool = False,
                help: str | None = None,
                metavar: str | tuple[str, ...] | None = sentinel,
                deprecated: bool = False,
            ) -> None: ...
        else:
            @overload
            def __init__(
                self,
                option_strings: Sequence[str],
                dest: str,
                default: bool | None = None,
                *,
                required: bool = False,
                help: str | None = None,
            ) -> None: ...
            @overload
            @deprecated("The `type`, `choices`, and `metavar` parameters are ignored and will be removed in Python 3.14.")
            def __init__(
                self,
                option_strings: Sequence[str],
                dest: str,
                default: _T | bool | None = None,
                type: Callable[[str], _T] | FileType | None = sentinel,
                choices: Iterable[_T] | None = sentinel,
                required: bool = False,
                help: str | None = None,
                metavar: str | tuple[str, ...] | None = sentinel,
            ) -> None: ...

else:
    class BooleanOptionalAction(Action):
        @overload
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            default: bool | None = None,
            *,
            required: bool = False,
            help: str | None = None,
        ) -> None: ...
        @overload
        @deprecated("The `type`, `choices`, and `metavar` parameters are ignored and will be removed in Python 3.14.")
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            default: _T | bool | None = None,
            type: Callable[[str], _T] | FileType | None = None,
            choices: Iterable[_T] | None = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
        ) -> None: ...

class Namespace(_AttributeHolder):
    def __init__(self, **kwargs: Any) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any, /) -> None: ...
    def __contains__(self, key: str) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    __hash__: ClassVar[None]  # type: ignore[assignment]

if sys.version_info >= (3, 14):
    @deprecated("Deprecated in Python 3.14; Simply open files after parsing arguments")
    class FileType:
        # undocumented
        _mode: str
        _bufsize: int
        _encoding: str | None
        _errors: str | None
        def __init__(
            self, mode: str = "r", bufsize: int = -1, encoding: str | None = None, errors: str | None = None
        ) -> None: ...
        def __call__(self, string: str) -> IO[Any]: ...

else:
    class FileType:
        # undocumented
        _mode: str
        _bufsize: int
        _encoding: str | None
        _errors: str | None
        def __init__(
            self, mode: str = "r", bufsize: int = -1, encoding: str | None = None, errors: str | None = None
        ) -> None: ...
        def __call__(self, string: str) -> IO[Any]: ...

# undocumented
class _ArgumentGroup(_ActionsContainer):
    title: str | None
    _group_actions: list[Action]
    if sys.version_info >= (3, 14):
        @overload
        def __init__(
            self,
            container: _ActionsContainer,
            title: str | None = None,
            description: str | None = None,
            *,
            argument_default: Any = ...,
            conflict_handler: str = ...,
        ) -> None: ...
        @overload
        @deprecated("Undocumented `prefix_chars` parameter is deprecated since Python 3.14.")
        def __init__(
            self,
            container: _ActionsContainer,
            title: str | None = None,
            description: str | None = None,
            *,
            prefix_chars: str,
            argument_default: Any = ...,
            conflict_handler: str = ...,
        ) -> None: ...
    else:
        def __init__(
            self,
            container: _ActionsContainer,
            title: str | None = None,
            description: str | None = None,
            *,
            prefix_chars: str = ...,
            argument_default: Any = ...,
            conflict_handler: str = ...,
        ) -> None: ...

# undocumented
class _MutuallyExclusiveGroup(_ArgumentGroup):
    required: bool
    _container: _ActionsContainer
    def __init__(self, container: _ActionsContainer, required: bool = False) -> None: ...

# undocumented
class _StoreAction(Action): ...

# undocumented
class _StoreConstAction(Action):
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            const: Any | None = None,
            default: Any = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
            deprecated: bool = False,
        ) -> None: ...
    elif sys.version_info >= (3, 11):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            const: Any | None = None,
            default: Any = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            const: Any,
            default: Any = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
        ) -> None: ...

# undocumented
class _StoreTrueAction(_StoreConstAction):
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            default: bool = False,
            required: bool = False,
            help: str | None = None,
            deprecated: bool = False,
        ) -> None: ...
    else:
        def __init__(
            self, option_strings: Sequence[str], dest: str, default: bool = False, required: bool = False, help: str | None = None
        ) -> None: ...

# undocumented
class _StoreFalseAction(_StoreConstAction):
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            default: bool = True,
            required: bool = False,
            help: str | None = None,
            deprecated: bool = False,
        ) -> None: ...
    else:
        def __init__(
            self, option_strings: Sequence[str], dest: str, default: bool = True, required: bool = False, help: str | None = None
        ) -> None: ...

# undocumented
class _AppendAction(Action): ...

# undocumented
class _ExtendAction(_AppendAction): ...

# undocumented
class _AppendConstAction(Action):
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            const: Any | None = None,
            default: Any = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
            deprecated: bool = False,
        ) -> None: ...
    elif sys.version_info >= (3, 11):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            const: Any | None = None,
            default: Any = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            const: Any,
            default: Any = None,
            required: bool = False,
            help: str | None = None,
            metavar: str | tuple[str, ...] | None = None,
        ) -> None: ...

# undocumented
class _CountAction(Action):
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            default: Any = None,
            required: bool = False,
            help: str | None = None,
            deprecated: bool = False,
        ) -> None: ...
    else:
        def __init__(
            self, option_strings: Sequence[str], dest: str, default: Any = None, required: bool = False, help: str | None = None
        ) -> None: ...

# undocumented
class _HelpAction(Action):
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str = "==SUPPRESS==",
            default: str = "==SUPPRESS==",
            help: str | None = None,
            deprecated: bool = False,
        ) -> None: ...
    else:
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str = "==SUPPRESS==",
            default: str = "==SUPPRESS==",
            help: str | None = None,
        ) -> None: ...

# undocumented
class _VersionAction(Action):
    version: str | None
    if sys.version_info >= (3, 13):
        def __init__(
            self,
            option_strings: Sequence[str],
            version: str | None = None,
            dest: str = "==SUPPRESS==",
            default: str = "==SUPPRESS==",
            help: str | None = None,
            deprecated: bool = False,
        ) -> None: ...
    elif sys.version_info >= (3, 11):
        def __init__(
            self,
            option_strings: Sequence[str],
            version: str | None = None,
            dest: str = "==SUPPRESS==",
            default: str = "==SUPPRESS==",
            help: str | None = None,
        ) -> None: ...
    else:
        def __init__(
            self,
            option_strings: Sequence[str],
            version: str | None = None,
            dest: str = "==SUPPRESS==",
            default: str = "==SUPPRESS==",
            help: str = "show program's version number and exit",
        ) -> None: ...

# undocumented
class _SubParsersAction(Action, Generic[_ArgumentParserT]):
    _ChoicesPseudoAction: type[Any]  # nested class
    _prog_prefix: str
    _parser_class: type[_ArgumentParserT]
    _name_parser_map: dict[str, _ArgumentParserT]
    choices: dict[str, _ArgumentParserT]
    _choices_actions: list[Action]
    def __init__(
        self,
        option_strings: Sequence[str],
        prog: str,
        parser_class: type[_ArgumentParserT],
        dest: str = "==SUPPRESS==",
        required: bool = False,
        help: str | None = None,
        metavar: str | tuple[str, ...] | None = None,
    ) -> None: ...

    # Note: `add_parser` accepts all kwargs of `ArgumentParser.__init__`. It also
    # accepts its own `help` and `aliases` kwargs.
    if sys.version_info >= (3, 14):
        def add_parser(
            self,
            name: str,
            *,
            deprecated: bool = False,
            help: str | None = ...,
            aliases: Sequence[str] = ...,
            # Kwargs from ArgumentParser constructor
            prog: str | None = ...,
            usage: str | None = ...,
            description: str | None = ...,
            epilog: str | None = ...,
            parents: Sequence[_ArgumentParserT] = ...,
            formatter_class: _FormatterClass = ...,
            prefix_chars: str = ...,
            fromfile_prefix_chars: str | None = ...,
            argument_default: Any = ...,
            conflict_handler: str = ...,
            add_help: bool = True,
            allow_abbrev: bool = True,
            exit_on_error: bool = True,
            suggest_on_error: bool = False,
            color: bool = False,
            **kwargs: Any,  # Accepting any additional kwargs for custom parser classes
        ) -> _ArgumentParserT: ...
    elif sys.version_info >= (3, 13):
        def add_parser(
            self,
            name: str,
            *,
            deprecated: bool = False,
            help: str | None = ...,
            aliases: Sequence[str] = ...,
            # Kwargs from ArgumentParser constructor
            prog: str | None = ...,
            usage: str | None = ...,
            description: str | None = ...,
            epilog: str | None = ...,
            parents: Sequence[_ArgumentParserT] = ...,
            formatter_class: _FormatterClass = ...,
            prefix_chars: str = ...,
            fromfile_prefix_chars: str | None = ...,
            argument_default: Any = ...,
            conflict_handler: str = ...,
            add_help: bool = True,
            allow_abbrev: bool = True,
            exit_on_error: bool = True,
            **kwargs: Any,  # Accepting any additional kwargs for custom parser classes
        ) -> _ArgumentParserT: ...
    else:
        def add_parser(
            self,
            name: str,
            *,
            help: str | None = ...,
            aliases: Sequence[str] = ...,
            # Kwargs from ArgumentParser constructor
            prog: str | None = ...,
            usage: str | None = ...,
            description: str | None = ...,
            epilog: str | None = ...,
            parents: Sequence[_ArgumentParserT] = ...,
            formatter_class: _FormatterClass = ...,
            prefix_chars: str = ...,
            fromfile_prefix_chars: str | None = ...,
            argument_default: Any = ...,
            conflict_handler: str = ...,
            add_help: bool = True,
            allow_abbrev: bool = True,
            exit_on_error: bool = True,
            **kwargs: Any,  # Accepting any additional kwargs for custom parser classes
        ) -> _ArgumentParserT: ...

    def _get_subactions(self) -> list[Action]: ...

# undocumented
class ArgumentTypeError(Exception): ...

# undocumented
def _get_action_name(argument: Action | None) -> str | None: ...
