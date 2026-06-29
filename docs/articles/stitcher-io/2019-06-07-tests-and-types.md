# Tests and types

URL: https://stitcher.io/blog/tests-and-types
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2019-06-07
Status: curated-processed
Topics: type-safety, testing, domain-modeling

## Why This Helps Programming
Shows why tests and types solve different parts of correctness. Types narrow the input space; tests still prove business behavior.

## Guidelines
### Use types to remove whole classes of tests
A type signature can rule out nulls, strings, missing arguments, and other invalid shapes before business logic runs. Keep tests for behavior the type system cannot express.

### Turn business ranges into domain types when the primitive is too wide
An integer type is still too broad for values such as RGB components, percentages, quantities, or ratings. Wrap constrained values in small domain objects when the range matters in more than one place.

### Do not claim types replace tests
Types improve program correctness, but business correctness still needs examples. Use both: types for shape and invariants, tests for outcomes and workflows.

## Examples
### Constrained value object
Use a domain type when a primitive permits invalid business values.

```php
<?php

final readonly class Rating
{
    public function __construct(public int $value)
    {
        if ($value < 1 || $value > 5) {
            throw new InvalidArgumentException('Rating must be between 1 and 5.');
        }
    }
}
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
