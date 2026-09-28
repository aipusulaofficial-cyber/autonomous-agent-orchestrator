from runtime_evidence import runtime_evidence
import time

def test_foundation_contract():
    e=runtime_evidence(request_id="foundation",stage="agent",decision="ALLOW",started=time.perf_counter())
    assert e["stage"] == "agent"
    assert e["trace_id"]
