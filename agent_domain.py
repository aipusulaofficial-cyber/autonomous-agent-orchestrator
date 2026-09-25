from dataclasses import dataclass
from enum import StrEnum


class TaskState(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    id: str
    state: TaskState = TaskState.PENDING
    attempts: int = 0

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("task id is required")
        if self.attempts < 0:
            raise ValueError("attempts must be non-negative")

    def start(self) -> None:
        if self.state is not TaskState.PENDING:
            raise ValueError("task not pending")
        self.state = TaskState.RUNNING
        self.attempts += 1

    def finish(self, ok: bool) -> None:
        if self.state is not TaskState.RUNNING:
            raise ValueError("task not running")
        self.state = TaskState.SUCCEEDED if ok else TaskState.FAILED

    def cancel(self) -> None:
        if self.state not in {TaskState.PENDING, TaskState.RUNNING}:
            raise ValueError("task cannot be cancelled")
        self.state = TaskState.CANCELLED


def enforce_step_budget(completed: int, limit: int) -> None:
    if completed < 0 or limit < 1:
        raise ValueError("invalid step budget")
    if completed >= limit:
        raise RuntimeError("agent step budget exhausted")
