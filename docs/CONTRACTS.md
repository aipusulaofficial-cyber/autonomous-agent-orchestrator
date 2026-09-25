# Contracts

Core domain: task graph/bounded execution/tool policy/recovery.

- API contract: versioned request/response schema.
- Domain contract: invariants and deterministic transitions.
- Provider contract: adapter interface, timeout/error taxonomy and normalized results.
- Event contract: versioned envelope for asynchronous flows.
- Configuration contract: bounded, validated configuration.

Breaking compatibility requires explicit tests and an ADR.