import json
import logging
import os
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_observability():
    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": "autonomous-agent-orchestrator",
                "deployment.environment": os.getenv("ENVIRONMENT", "local"),
            }
        )
    )
    if os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )

            provider.add_span_processor(
                BatchSpanProcessor(
                    OTLPSpanExporter(endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"])
                )
            )
        except ImportError:
            provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    else:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(
            {
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
            }
        )


def get_logger(name):
    h = logging.StreamHandler()
    h.setFormatter(JsonFormatter())
    l = logging.getLogger(name)
    l.handlers[:] = [h]
    l.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return l


class PrincipalObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        correlation_id = request.headers.get("x-correlation-id") or request_id
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = (time.perf_counter() - start) * 1000
        response.headers["x-request-id"] = request_id
        response.headers["x-correlation-id"] = correlation_id
        response.headers["x-latency-ms"] = f"{elapsed:.3f}"
        return response
