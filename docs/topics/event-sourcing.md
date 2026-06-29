# Event Sourcing

## The Short Version
Use event streams when history, auditability, temporal reporting, or process reconstruction is central to the domain.

## Practical Rules
- Do not event-source every table by default.
- Name events as facts that already happened.
- Keep projections rebuildable and free of irreversible business writes.
- Use ordinary stateful models for parts of the system that do not benefit from history.

## Tips And Tricks
### Choose event sourcing by domain need, not application size
The question is whether the workflow needs historical facts and replayable state, not whether the project is large enough to justify a pattern. ([source](../articles/stitcher-io/2021-04-09-what-event-sourcing-is-not-about.md))

### Mix event-sourced and stateful models deliberately
Admin CRUD, lookup tables, and simple configuration often work better as normal state. Money movement, order flows, and audit-heavy domains may justify event streams. ([source](../articles/stitcher-io/2020-04-14-combining-event-sourcing-and-stateful-systems.md))

### Use event queries before permanent projections when reads are occasional
A projection has maintenance cost. If a read is infrequent, querying the stream directly can be simpler until usage proves otherwise. ([source](../articles/stitcher-io/2021-06-15-a-new-major-version-of-laravel-event-sourcing.md))

## Examples
### Fact event and projection
The event records what happened; the projection answers a read question.

```php
<?php

final readonly class OrderWasPaid
{
    public function __construct(
        public string $orderId,
        public Money $amount,
        public DateTimeImmutable $paidAt,
    ) {}
}

final class OrdersToShipProjector
{
    public function onOrderWasPaid(OrderWasPaid $event): void
    {
        OrdersToShip::query()->create([
            'order_id' => $event->orderId,
            'paid_at' => $event->paidAt,
        ]);
    }
}
```

## Source Videos
- No source videos have been linked yet.

## Source Articles
- [Starting with event sourcing](../articles/stitcher-io/2021-04-09-what-event-sourcing-is-not-about.md)
- [Combining event sourcing and stateful systems](../articles/stitcher-io/2020-04-14-combining-event-sourcing-and-stateful-systems.md)
- [A new major version of Laravel Event Sourcing](../articles/stitcher-io/2021-06-15-a-new-major-version-of-laravel-event-sourcing.md)

## Related Topics
- [Database Integrity](database-integrity.md)
- [Domain Modeling In PHP](domain-modeling.md)
- [Testing Strategy](testing.md)
