import datetime
import inspect
from contextlib import contextmanager
from typing import Iterator, Callable, Any

from approvaltests.utilities.string_wrapper import StringWrapper
from approvaltests.namer import StackFrameNamer


class Toggles:
    def __init__(self, show: bool):
        self.query = show
        self.message = show
        self.variable = show



class LoggingInstance:
    def __init__(self):
        self.toggles = Toggles(True)
        self.previous_timestamp = None
        self.logger = lambda t: print(t, end="")
        self.tabbing = 0
        self.counter = 0
        self.log_with_timestamps = True
        self.timer: Callable[[], datetime.datetime] = datetime.datetime.now

    def log_to_string(self) -> StringWrapper:
        buffer = StringWrapper()
        self.logger = buffer.append
        self.log_with_timestamps = False
        return buffer

    @contextmanager
    def use_markers(self, additional_stack: int = 0) -> Iterator[None]:
        stack_position = 1 + additional_stack
        stack = inspect.stack(stack_position)[2]
        method_name = stack.function
        filename = StackFrameNamer.get_class_name_for_frame(stack)
        expected = f"-> in: {method_name}(){filename}"
        self.log_line(expected)
        self.tabbing = self.tabbing + 1
        yield
        self.tabbing = self.tabbing - 1
        expected = f"<- out: {method_name}(){filename}"
        self.log_line(expected)
        pass

    def log_line(self, text: str, use_timestamps=True) -> None:
        if self.counter != 0:
            self.logger("\n")
            self.counter = 0
        timestamp = self.get_timestamp() if use_timestamps else ""
        output_message = f"{timestamp}{self.get_tabs()}{text}\n"
        self.logger(output_message)

    def get_timestamp(self) -> str:
        timestamp = ""
        if self.log_with_timestamps:
            time1: datetime.datetime = self.timer()
            time = time1.strftime("%Y-%m-%dT%H:%M:%SZ")
            diff_millseconds = 0
            if self.previous_timestamp != None:
                delta = time1 - self.previous_timestamp
                diff_millseconds = int((delta).total_seconds() * 1000)
            diff = diff_millseconds
            diff_display = f" ~{diff:06}ms"
            timestamp = f"[{time} {diff_display}] "
            self.previous_timestamp = time1
        return timestamp


    def hour_glass(self) -> None:
        self.increment_hour_glass_counter()
        if self.counter == 1:
            self.logger(f"{self.get_tabs()}.")
        elif self.counter == 100:
            self.logger("10\n")
            self.counter = 0
        elif self.counter % 10 == 0:
            digit = int(self.counter / 10)
            self.logger(f"{digit}")
        else:
            self.logger(".")

    def get_tabs(self) -> str:
        return "  " * self.tabbing

    def increment_hour_glass_counter(self) -> None:
        self.counter = self.counter + 1

    def variable(self, name: str, value: Any) -> None:
        if not self.toggles.variable:
            return
        self.log_line(f"variable: {name} = {value}")

    def event(self, event_name: str) -> None:
        self.log_line(f"event: {event_name}")

    def query(self, query_text: str) -> None:
        if not self.toggles.query:
            return
        self.log_line(f"Sql: {query_text}")

    def message(self, message):
        if not self.toggles.message:
            return
        self.log_line(f"message: {message}")

    def warning(self, exception: Exception) -> None:
        warning_stars = "*" * 91
        self.log_line(warning_stars, use_timestamps=False)
        if self.log_with_timestamps:
            self.log_line("", use_timestamps=True)
        self.log_line(str(exception), use_timestamps=False)
        self.log_line(warning_stars, use_timestamps=False)

    def show_query(self, show):
        self.toggles.query = show

    def show_all(self, show: bool) -> None:
        self.toggles = Toggles(show)

    def show_message(self, show):
        self.toggles.message = show

    def show_variable(self, show):
        self.toggles.variable = show