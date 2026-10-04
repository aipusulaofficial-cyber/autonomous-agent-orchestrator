"""Bounded agent orchestration: explicit states, tool policy and audit trail."""

from dataclasses import dataclass, field
from enum import StrEnum


class State(StrEnum):
    PLANNED = "planned"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    steps: list[str]
    state: State = State.PLANNED
    audit: list[str] = field(default_factory=list)


class Orchestrator:
    def __init__(self, tools, max_steps=8):
        if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 1:
            raise ValueError("max_steps must be a positive integer")
        if not isinstance(tools, dict) or any(not callable(tool) for tool in tools.values()):
            raise ValueError("tools must be a mapping of callables")
        self.tools = tools
        self.max_steps = max_steps

    def run(self, t):
        if t.state is not State.PLANNED:
            raise ValueError("task is not runnable from its current state")
        if not isinstance(t.id, str) or not t.id.strip():
            raise ValueError("task id is required")
        if not isinstance(t.steps, list) or any(
            not isinstance(step, str) or not step for step in t.steps
        ):
            raise ValueError("task steps must be non-empty strings")
        if len(t.steps) > self.max_steps:
            raise ValueError("step budget exceeded")
        t.state = State.RUNNING
        t.audit.append("started")
        try:
            for name in t.steps:
                if name not in self.tools:
                    raise KeyError(f"tool not allowed: {name}")
                self.tools[name]()
                t.audit.append("tool:" + name)
            t.state = State.SUCCEEDED
            t.audit.append("completed")
        except Exception as e:
            t.state = State.FAILED
            t.audit.append("failed:" + type(e).__name__)
            raise
        return t
