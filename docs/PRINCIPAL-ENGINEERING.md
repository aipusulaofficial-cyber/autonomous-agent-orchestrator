# Principal Engineering Contract

## Scope
This document defines the engineering decisions that make this repository reviewable as a production-oriented reference implementation.

## Core boundary
**Primary concern:** Agent orchestration.

Keep planning, policy, tool invocation, and state management behind explicit interfaces; bound tool calls and execution time; make retries idempotency-aware; preserve an execution audit trail.

## Non-functional requirements
- **Determinism:** core behavior should be reproducible in tests without live external services.
- **Failure semantics:** expected failure classes must be explicit and observable; hidden retries are avoided.
- **Security:** validate untrusted inputs, use safe defaults, minimize privilege at boundaries, and run deployed workloads as non-root with RuntimeDefault seccomp.
- **Operability:** expose health/readiness signals where applicable and preserve enough context to diagnose failures.
- **Change safety:** CI, production tests, and security/SBOM checks are release gates for the configured repository workflows.

## Enforced controls
- GitHub Actions use read-only repository permissions, explicit timeouts, and immutable commit-pinned third-party actions.
- Checkout does not persist GitHub credentials.
- Kubernetes, Helm, and Terraform definitions use non-root UID/GID 10001, RuntimeDefault seccomp, no privilege escalation, read-only root filesystems, dropped capabilities, bounded resources, and health probes.
- Deployment images use versioned `0.1.0` instead of `latest`.
- Security/SBOM runs filesystem vulnerability scanning and CycloneDX SBOM generation.

## Review checklist
- [x] Public contracts are validated.
- [x] Domain policy is independent from infrastructure adapters.
- [x] Failure and retry behavior is explicit.
- [x] Resource limits are bounded where work can grow.
- [x] Tests cover happy path, invalid input, and representative failure paths.
- [x] Security-sensitive decisions are auditable.
- [x] CI validates the repository before merge.
- [x] Architecture trade-offs are documented rather than implied.
- [x] Deployment manifests enforce least privilege and bounded resources.
- [x] Supply-chain actions are pinned to immutable commits.

## Evidence boundary
**GREEN** means the configured CI, production-tests, and security/SBOM gates pass on the current main commit. It is repository-level engineering evidence, not environment-independent production certification.

## Production boundary
This remains a reference implementation; production deployment requires environment-specific SLOs, capacity planning, secrets management, dependency hardening, and operational ownership.
