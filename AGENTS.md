# Pathwise Agent Guidelines

## Human governance

- Pathwise is human-governed. Approved architecture and explicitly approved engineering decisions are authoritative.
- Agents implement bounded, approved work and do not silently redesign the system.
- Escalate meaningful architecture or tooling decisions instead of assuming them.

## Architecture guardrails

- Preserve the approved direction: React with Vite for the frontend; Python with FastAPI for the backend; a backend Modular Monolith; and PostgreSQL as the canonical application data direction.
- Do not independently introduce microservices; Kubernetes or Helm as Production architecture; another canonical database or authentication architecture; Redis or cache infrastructure; a dedicated Search platform; queues, workers, or event buses; persistent Staging; or speculative distributed-system components.

## Scope and simplicity

- Implement only the approved task or increment, using the smallest clear implementation that satisfies it.
- Do not create speculative abstractions or enterprise-style layers without a current need.
- Do not solve later roadmap stages or registered Open Questions before their approved resolution stage.

## Dependencies and security

- Add runtime or Production dependencies only when approved by the task or explicit escalation.
- Never add real secrets, tokens, AWS credentials, Cognito secrets, or Production credentials, and do not intentionally expose secret material in logs or command output.
- Do not independently redesign authentication, authorization, persistence, or security strategy.

## Repository safety

- Preserve unrelated user changes and do not perform destructive Git operations.
- Do not commit, push, merge, or create a pull request unless explicitly requested.
- Review the resulting diff and run relevant validation after implementation.

## Stop and escalate

Stop and report rather than deciding independently when work requires an architecture change, an unapproved runtime dependency, a new infrastructure component, a changed domain boundary, a persistence/authentication/security strategy change, significant scope expansion, contradiction of an ADR or approved architecture, early resolution of an Open Question, or access to real secrets or Production credentials.

At the end of work, report files changed, commands executed, validation results, assumptions, unresolved problems, and possible architecture conflicts.
