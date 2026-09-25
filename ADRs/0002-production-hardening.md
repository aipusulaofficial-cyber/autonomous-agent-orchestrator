# ADR-0002: Production hardening
The HTTP edge is isolated from domain execution. OpenTelemetry traces requests. Kubernetes probes and bounded resources make failure states visible; Helm packages the workload; Terraform owns infrastructure inputs. Trivy/CycloneDX gate supply-chain risk; contract/property tests protect input boundaries; Locust validates baseline load.
Production externalizes state, secrets, telemetry collectors and autoscaling.
