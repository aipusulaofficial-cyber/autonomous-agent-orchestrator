"""Bounded agent orchestration: explicit states, tool policy and audit trail."""

from dataclasses import dataclass, field
from enum import Enum


class State(str, Enum):
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
        self.tools = tools
        self.max_steps = max_steps

    def run(self, t):
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
