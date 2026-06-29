# Extend or implement

URL: https://stitcher.io/blog/extends-vs-implements
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2024-08-21
Status: curated-processed
Topics: object-design, architecture, ddd

## Why This Helps Programming
Offers a useful mental model for inheritance versus interfaces: inherit for real domain identity, implement for technical capability.

## Guidelines
### Use inheritance for true specialization, not framework convenience
If a class is not really a subtype in the domain, prefer composition or an interface. Framework base classes can be practical, but do not let them define your domain model language.

### Use interfaces for acts-as capabilities
An interface says the object can perform a role in this context. That is different from saying the object is fundamentally that thing.

## Examples
### Capability interface
A model may act as billable without making billing its whole identity.

```php
<?php

interface Billable
{
    public function billingReference(): string;
}

final class Team implements Billable
{
    public function billingReference(): string
    {
        return 'team:' . $this->id;
    }
}
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
