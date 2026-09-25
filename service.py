from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field

from agent_domain import Task
from observability import configure_observability, get_logger

configure_observability()
logger = get_logger(__name__)
tracer = trace.get_tracer("autonomous-agent-orchestrator")

app = FastAPI(title="autonomous-agent-orchestrator", version="1.0.0")


class TaskRequest(BaseModel):
    key: str
    payload: dict = Field(default_factory=dict)


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/v1/tasks")
def handle(request: TaskRequest) -> dict[str, str | int]:
    with tracer.start_as_current_span("agent.task.start") as span:
        span.set_attribute("agent.task_id", request.key)
        try:
            task = Task(request.key)
            task.start()
            logger.info(
                "agent_task_started",
                extra={"task_id": task.id, "attempts": task.attempts},
            )
            return {
                "task_id": task.id,
                "state": task.state,
                "attempts": task.attempts,
            }
        except ValueError as exc:
            logger.warning(
                "agent_task_rejected",
                extra={"task_id": request.key, "reason": str(exc)},
            )
            raise HTTPException(status_code=400, detail=str(exc)) from exc
