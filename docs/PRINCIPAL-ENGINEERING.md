# Principal Engineering Contract

## Scope
This document defines the engineering decisions that make this repository reviewable as a production-oriented reference implementation.

## Core boundary
**Primary concern:** Agent orchestration.

Keep planning, policy, tool invocation, and state management behind explicit interfaces; bound tool calls and execution time; make retries idempotency-aware; preserve an execution audit trail.

## Non-functional requirements
- **Determinism:** core behavior should be reproducible in tests without live external services.
- **Failure semantics:** expected failure classes must be explicit and observable; hidden retries are avoided.
- **Security:** validate untrusted inputs, use safe defaults, and minimize privilege at boundaries.
- **Operability:** expose health/readiness signals where applicable and preserve enough context to diagnose failures.
- **Change safety:** CI is a release gate; architecture changes should update relevant ADRs and tests.

## Review checklist
- [ ] Public contracts are validated.
- [ ] Domain policy is independent from infrastructure adapters.
- [ ] Failure and retry behavior is explicit.
- [ ] Resource limits are bounded where work can grow.
- [ ] Tests cover happy path, invalid input, and representative failure paths.
- [ ] Security-sensitive decisions are auditable.
- [ ] CI validates the repository before merge.
- [ ] Architecture trade-offs are documented rather than implied.

## Production boundary
This is a reference implementation. Production deployment still requires environment-specific SLOs, capacity planning, secrets management, dependency hardening, and operational ownership.
