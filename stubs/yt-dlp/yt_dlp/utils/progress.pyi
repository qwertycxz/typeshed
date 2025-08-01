class ProgressCalculator:
    SAMPLING_WINDOW: int
    SAMPLING_RATE: float
    GRACE_PERIOD: int
    downloaded: int
    elapsed: float
    speed: SmoothValue
    eta: SmoothValue
    def __init__(self, initial: int) -> None: ...
    @property
    def total(self) -> int | None: ...
    @total.setter
    def total(self, value: int | None) -> None: ...
    def thread_reset(self) -> None: ...
    def update(self, size: int | None) -> None: ...

class SmoothValue:
    value: float | None
    def __init__(self, initial: float | None, smoothing: float) -> None: ...
    smooth: float | None
    def set(self, value: float) -> None: ...
    def reset(self) -> None: ...
