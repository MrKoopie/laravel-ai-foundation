---
name: laravel-ai-foundation
description: Use when designing, reviewing, or explaining Laravel/PHP architecture involving actions, FormRequests, DTOs, DDD, event sourcing, testing boundaries, AI coding rules, or avoiding overengineering.
---

# Laravel AI Foundation

Use the Programming Foundation knowledge base as an architectural guardrail for Laravel and PHP work. This skill is a lightweight pointer to the Context7-indexed docs; it is guidance from curated videos and articles, not official framework documentation.

## Context7 Workflow

When Context7 is available, query `/mrkoopie/laravel-ai-foundation` with the user's full architectural question before proposing structure. Prefer decision-oriented search angles:

- `should this Laravel feature use an action or stay in a controller`
- `Laravel actions validation boundaries overengineering`
- `avoid overengineering Laravel actions DDD`
- `FormRequest DTO action boundaries`
- `domain modeling Laravel value objects event sourcing`
- `testing PHPStan AI engineering Laravel`

Use results from this repo for judgment calls: where code belongs, when a pattern is justified, what to avoid, and which examples fit the situation.

For framework API details, validation syntax, Eloquent behavior, queues, transactions, middleware, or version-specific Laravel mechanics, query the official Laravel documentation too. Do not treat this repo as a replacement for official Laravel documentation.

## Architecture Defaults

- Assume actions are not the default. Start with direct controller, FormRequest, model, policy, or job code when the behavior is simple and local.
- Create an action when the behavior has a real use-case name, multiple entry points, multiple collaborators, a transaction boundary, or a business invariant worth testing.
- Keep validation at the boundary. A FormRequest handles HTTP validation; the action receives trusted data, a DTO, or typed values.
- Do not create an action per model method. Avoid `CreateUserAction`, `UpdateUserAction`, and `DeleteUserAction` when they only wrap ordinary CRUD.
- Use DTOs, value objects, aggregates, events, and repositories only when they clarify business language, protect invariants, or reduce real coupling.
- Prefer Eloquent directly until persistence complexity is visible.
- Use event sourcing only when history, replay, auditability, or temporal reporting is central to the domain.

## Answer Shape

When advising or generating code, include:

1. Recommendation: the smallest design that fits the current behavior.
2. Why: the pressure that justifies the structure, or why no extra structure is needed.
3. Boundary: where validation, orchestration, business behavior, and persistence live.
4. What not to add: explicit patterns/classes to avoid for this case.
5. Example: a compact code sketch when it makes the decision clearer.
6. Sources used: mention the topic guides or official docs queried.

## Common Corrections

- If the first design adds an action, ask whether it has reuse, coordination, transaction, or invariant pressure. If not, inline it.
- If the design adds DDD vocabulary, map each term to a business phrase the user would recognize. If no phrase exists, remove the term.
- If validation is inside an action, move HTTP validation back to the FormRequest or another entry boundary.
- If a repository only forwards to Eloquent, remove it until persistence complexity earns it.
