# My PHP enum style guide

URL: https://stitcher.io/blog/php-enum-style-guide
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2022-05-30
Status: curated-processed
Topics: enums, domain-modeling, type-safety

## Why This Helps Programming
Gives practical enum rules that help PHP domain states stay expressive without adding unnecessary backing values or label coupling.

## Guidelines
### Use backed enums only when persistence or serialization needs a stable value
A pure enum is enough for in-code states. Add string or integer backing only when a database, API, queue payload, or external contract needs it.

### Keep display labels out of enum backing values
Backing values are technical contracts. UI labels are presentation concerns and should live in methods, translation files, or presenters.

### Allow simple behavior on enums
Small match-based methods can keep state-specific behavior close to the state while avoiding scattered switch statements.

## Examples
### Enum with behavior and separate label
Keep the stored value stable and the label replaceable.

```php
<?php

enum OrderStatus: string
{
    case DRAFT = 'draft';
    case PAID = 'paid';
    case CANCELLED = 'cancelled';

    public function canBeShipped(): bool
    {
        return $this === self::PAID;
    }

    public function label(): string
    {
        return __('orders.status.' . $this->value);
    }
}
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
