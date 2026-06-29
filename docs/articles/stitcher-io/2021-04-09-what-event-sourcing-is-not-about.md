# Starting with event sourcing

URL: https://stitcher.io/blog/what-event-sourcing-is-not-about
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2021-04-09
Status: curated-processed
Topics: event-sourcing, ddd, architecture

## Why This Helps Programming
Reframes event sourcing as a modeling choice, not only an enterprise-scale infrastructure pattern.

## Guidelines
### Use event sourcing for behavior that needs history, not for every table
The useful question is not whether the app is big enough. Ask whether the domain benefits from replayable facts, auditability, temporal reporting, or process reconstruction.

### Start from the event stream as the source of truth
In event-sourced code, state is derived from facts that happened. Name events in past tense and keep projections as read models, not as the primary record of truth.

## Examples
### Past-tense domain event
An event records a fact; commands and actions request work.

```php
<?php

final readonly class InvoiceWasPaid
{
    public function __construct(
        public string $invoiceId,
        public Money $amount,
        public DateTimeImmutable $paidAt,
    ) {}
}
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
