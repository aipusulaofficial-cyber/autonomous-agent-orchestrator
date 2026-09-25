from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from agent_domain import *
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"autonomous-agent-orchestrator"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="autonomous-agent-orchestrator",version="1.0.0");tracer=trace.get_tracer("autonomous-agent-orchestrator")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/tasks")
def handle(r:Request):
 with tracer.start_as_current_span("autonomous-agent-orchestrator.domain"):
  try: t=Task(r.key);t.start();return {"task_id":t.id,"state":t.state,"attempts":t.attempts}
  except (ValueError,KeyError,RuntimeError) as e: raise HTTPException(status_code=400,detail=str(e)) from e
