from typing import ClassVar

from docutils import writers

class Writer(writers.UnfilteredWriter[str]):
    supported: ClassVar[tuple[str, ...]]
    config_section: ClassVar[str]
    config_section_dependencies: ClassVar[tuple[str]]
    def translate(self) -> None: ...
