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
    max_attempts: int = 3

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("task id is required")
        if self.attempts < 0:
            raise ValueError("attempts must be non-negative")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        if self.attempts > self.max_attempts:
            raise ValueError("attempts cannot exceed max_attempts")

    def start(self) -> None:
        if self.state is not TaskState.PENDING:
            raise ValueError("task not pending")
        if self.attempts >= self.max_attempts:
            raise RuntimeError("task attempt budget exhausted")
        self.state = TaskState.RUNNING
        self.attempts += 1

    def finish(self, ok: bool) -> None:
        if self.state is not TaskState.RUNNING:
            raise ValueError("task not running")
        self.state = TaskState.SUCCEEDED if ok else TaskState.FAILED

    def retry(self) -> None:
        if self.state is not TaskState.FAILED:
            raise ValueError("only failed tasks can be retried")
        if self.attempts >= self.max_attempts:
            raise RuntimeError("task attempt budget exhausted")
        self.state = TaskState.PENDING

    def cancel(self) -> None:
        if self.state not in {TaskState.PENDING, TaskState.RUNNING}:
            raise ValueError("task cannot be cancelled")
        self.state = TaskState.CANCELLED


@dataclass(frozen=True)
class ToolPolicy:
    allowed_tools: frozenset[str]
    max_steps: int = 20

    def __post_init__(self) -> None:
        if self.max_steps < 1:
            raise ValueError("max_steps must be positive")
        if any(not tool.strip() for tool in self.allowed_tools):
            raise ValueError("tool names must be non-empty")

    def authorize(self, tool: str) -> None:
        if not tool.strip():
            raise ValueError("tool name is required")
        if tool not in self.allowed_tools:
            raise PermissionError("tool is not allowed")


def enforce_step_budget(completed: int, limit: int) -> None:
    if completed < 0 or limit < 1:
        raise ValueError("invalid step budget")
    if completed >= limit:
        raise RuntimeError("agent step budget exhausted")
