# Domain Modeling In PHP

## The Short Version
Use types, enums, value objects, and clear object relationships to make business rules explicit.

## Practical Rules
- Promote primitives to value objects when a business constraint is reused or easy to violate.
- Use enums for named states; add backing values only for persistence or serialization.
- Use inheritance for true specialization and interfaces for acts-as capabilities.
- Avoid clever abstractions before the real business variation is visible.

## Tips And Tricks
### Let domain types narrow invalid input
A primitive such as `int` or `string` usually permits values the business does not. Small value objects make those invalid states unrepresentable after construction. ([source](../articles/stitcher-io/2019-06-07-tests-and-types.md))

### Keep enum values technical
Enum backing values should be stable persistence or serialization contracts. Labels belong in translation, presentation, or enum methods. ([source](../articles/stitcher-io/2022-05-30-php-enum-style-guide.md))

### Distinguish is-a from acts-as
Inheritance should describe true domain specialization. Interfaces are better for technical roles such as billable, searchable, exportable, or publishable. ([source](../articles/stitcher-io/2024-08-21-extends-vs-implements.md))

## Examples
### Value object plus enum
Types carry business language across actions, jobs, tests, and models.

```php
<?php

final readonly class Percentage
{
    public function __construct(public int $value)
    {
        if ($value < 0 || $value > 100) {
            throw new InvalidArgumentException('Percentage must be between 0 and 100.');
        }
    }
}

enum DiscountType: string
{
    case FIXED = 'fixed';
    case PERCENTAGE = 'percentage';

    public function requiresPercentage(): bool
    {
        return $this === self::PERCENTAGE;
    }
}
```

## Source Videos
- [Why use DTOs? Data Transfer Objects](../videos/2025-04-02-why-use-dtos-data-transfer-objects-c6CP1C8liyU.md)

## Source Articles
- [Tests and types](../articles/stitcher-io/2019-06-07-tests-and-types.md)
- [My PHP enum style guide](../articles/stitcher-io/2022-05-30-php-enum-style-guide.md)
- [Extend or implement](../articles/stitcher-io/2024-08-21-extends-vs-implements.md)
- [Don't be clever](../articles/stitcher-io/2023-06-02-dont-be-clever.md)

## Related Topics
- [Request Data Boundaries](request-data-boundaries.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
- [Clean Laravel Code](clean-code.md)
