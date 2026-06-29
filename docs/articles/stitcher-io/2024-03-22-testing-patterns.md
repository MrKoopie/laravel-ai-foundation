# Testing Patterns

URL: https://stitcher.io/blog/testing-patterns
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2024-03-22
Status: curated-processed
Topics: testing, maintainability

## Why This Helps Programming
Shows how test design affects whether people keep adding tests when the number of cases grows.

## Guidelines
### Reduce test friction for repeated cases
When dozens of similar behaviors need coverage, move the common assertion shape into a reusable test helper and keep each case close to the behavior it documents.

### Avoid a giant data-provider dumping ground
Centralized data providers can reduce duplication but become hard to navigate. Prefer distributed fixtures or per-feature cases when the list grows large.

### Make test failures point to the broken case
A scalable test pattern should make it obvious which input, class, or pattern failed without making the developer search through a shared table.

## Examples
### Case object for repeated tests
Keep each case named and close to the domain concept being tested.

```php
<?php

it('parses invoice numbers', function (string $input, string $expected) {
    expect(InvoiceNumber::fromString($input)->value)->toBe($expected);
})->with([
    'plain number' => ['INV-1001', 'INV-1001'],
    'lowercase prefix' => ['inv-1001', 'INV-1001'],
]);
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
