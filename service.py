import time

from fastapi import FastAPI, HTTPException
from fastapi import Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel, Field

from agent_domain import Task
from observability import PrincipalObservabilityMiddleware, configure_observability, get_logger
from runtime_evidence import request_id_from_headers, runtime_evidence

configure_observability()
logger = get_logger(__name__)
tracer = trace.get_tracer("autonomous-agent-orchestrator")
app = FastAPI(title="autonomous-agent-orchestrator", version="1.0.0")
app.add_middleware(PrincipalObservabilityMiddleware)


class TaskRequest(BaseModel):
    key: str = Field(min_length=1, max_length=128)


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/tasks")
def handle(request: TaskRequest, http_request: FastAPIRequest):
    started = time.perf_counter()
    request_id = request_id_from_headers(http_request.headers)
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
                "evidence": runtime_evidence(
                    request_id=request_id,
                    stage="agent.task.start",
                    decision="ALLOW",
                    started=started,
                    retry_count=task.attempts,
                ),
            }
        except ValueError as exc:
            evidence = runtime_evidence(
                request_id=request_id,
                stage="agent.task.start",
                decision="DENY",
                started=started,
                error=str(exc),
            )
            logger.warning(
                "agent_task_rejected",
                extra={"task_id": request.key, "reason": str(exc)},
            )
            raise HTTPException(
                status_code=400,
                detail={"error": str(exc), "evidence": evidence},
            ) from exc
