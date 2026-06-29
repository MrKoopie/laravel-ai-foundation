# Avoid Overengineering

## The Short Version
Add structure only when it makes Laravel and PHP code easier to change, test, reuse, or reason about.

## Practical Rules
- Start with direct Laravel code when behavior is simple, local, and obvious.
- Wait for pressure before adding patterns: repeated behavior, multiple entry points, hidden business rules, or coordination across collaborators.
- Add an action only when the behavior has earned a name, not because every controller line needs a class.
- Use DDD terms only when they clarify business language the team actually uses.
- Prefer deleting unnecessary states, flags, and indirection before adding more coordination code.

## Tips And Tricks
### Wait for pressure before adding patterns
A pattern should pay rent. If a small exception needs flags, hooks, base classes, or override methods, the abstraction may be more expensive than the duplication it removed. ([source](../articles/stitcher-io/2023-06-02-dont-be-clever.md))

### Use actions after the use case appears
Actions are not the default destination for code. Add one when a behavior has a real use-case name, needs reuse outside HTTP, coordinates multiple collaborators, or owns a transaction boundary. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

### Keep persistence boring until it hurts
Do not add repositories, query buses, or data mappers around ordinary Eloquent calls unless persistence complexity is already making callers harder to test or change. ([source](../articles/stitcher-io/2025-10-22-reducing-code-motion.md))

### Do not let DDD become decoration
Value objects, aggregates, events, and policies help when they express domain language or protect invariants. They are noise when they only rename framework operations. ([source](../articles/stitcher-io/2019-06-07-tests-and-types.md))

## Examples
### What not to add
For a one-screen admin form, skip an action, DTO hierarchy, repository, command bus, event stream, and module boundary unless the behavior shows real pressure for them.

```text
Use the smallest design that explains the current behavior:
- FormRequest for HTTP validation
- Controller for HTTP orchestration
- Eloquent model call for the single write
- Focused test for the user-visible result
```

### Small controller before abstraction
This code has no reuse pressure, no multi-step consistency boundary, and no hidden domain rule. Keeping it direct makes the behavior easier to scan.

```php
<?php

final class StoreLabelController
{
    public function __invoke(StoreLabelRequest $request): RedirectResponse
    {
        $label = Label::query()->create($request->validated());

        return redirect()->route('labels.show', $label);
    }
}
```

### Extraction when pressure appears
Once the same behavior is needed from HTTP and a queued import, and it has a consistency rule, the action earns its place.

```php
<?php

final readonly class RegisterSubscriber
{
    public function handle(SubscriberData $data): Subscriber
    {
        return DB::transaction(function () use ($data) {
            $subscriber = Subscriber::query()->create($data->toArray());

            SubscribeToDefaultList::dispatchSync($subscriber);

            return $subscriber;
        });
    }
}
```

## Source Videos
- [The Action Pattern Is Key to Clean Code](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md)
- [Clean Laravel Controllers with Actions and Form Requests](../videos/2025-01-29-clean-laravel-controllers-with-actions-and-form-requests-nLNdQ9q_RxA.md)

## Source Articles
- [Don't be clever](../articles/stitcher-io/2023-06-02-dont-be-clever.md)
- [Reducing code motion](../articles/stitcher-io/2025-10-22-reducing-code-motion.md)
- [Strategies](../articles/stitcher-io/2022-04-06-strategies.md)
- [What event sourcing is not about](../articles/stitcher-io/2021-04-09-what-event-sourcing-is-not-about.md)

## Related Topics
- [Laravel Actions](laravel-actions.md)
- [Domain Modeling In PHP](domain-modeling.md)
- [Event Sourcing](event-sourcing.md)
- [Dependencies And Maintenance](dependencies-and-maintenance.md)
