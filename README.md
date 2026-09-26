# Autonomous Agent Orchestrator

An orchestration runtime for policy-controlled agent planning, tool execution, state propagation and recovery.

## Execution lifecycle
```text
request -> policy validation -> plan -> bounded tool execution -> state update -> recovery/retry -> final outcome + audit context
```

## Core boundaries
- **Planning** creates an execution plan under explicit policy.
- **Tool boundary** prevents arbitrary infrastructure access from leaking into the domain layer.
- **State boundary** keeps execution context explicit across steps.
- **Recovery policy** defines which failures can be retried or resumed.
- **Audit context** makes execution decisions reviewable.

## Reliability
Tool calls and execution time are bounded. Recovery is policy-driven and idempotency-aware; dependency failure is not converted into a false success.

## Security
Policy controls tool access and validation occurs before execution. Sensitive operational context is separated from user-visible results.

## Verification
Contract, edge-case and failure-path tests are part of CI, alongside security and production validation.

## Evidence
[ARCHITECTURE.md](ARCHITECTURE.md) · [docs/PRINCIPAL-ENGINEERING.md](docs/PRINCIPAL-ENGINEERING.md) · [ADRs](ADRs/)

This project is an execution orchestrator, not merely an agent prompt collection.