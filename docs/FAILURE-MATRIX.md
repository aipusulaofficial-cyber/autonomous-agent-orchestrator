# Failure matrix

| Failure | Detection | Action | Retry? | Impact |
|---|---|---|---|---|
| Invalid input | validation | reject | No | 4xx |
| Dependency timeout | timeout budget | normalize | Safe/idempotent only | bounded failure/degradation |
| Dependency error | adapter | exponential backoff | Safe/idempotent only | bounded latency |
| Repeated failure | circuit breaker | open circuit | No while open | fast failure |
| Overload | bounded executor/rate limiter | fail fast/degrade | No | 429/degraded |
| Telemetry failure | exporter error | preserve domain result | exporter-local | no domain corruption |

Tool timeout -> bounded retry only when idempotent; policy denial -> fail closed; repeated tool failure -> circuit open; graph execution is bounded by step/time budgets.