# Uncertainty, doubt, and static analysis

URL: https://stitcher.io/blog/uncertainty-doubt-and-static-analysis
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2022-07-16
Status: curated-processed
Topics: type-safety, static-analysis, tooling

## Why This Helps Programming
Makes the case that modern PHP projects should lean into opt-in strictness instead of treating dynamic PHP as the default forever.

## Guidelines
### Use static analysis as design feedback
PHPStan, Psalm, and IDE inspections are not only bug finders. They expose unclear shapes, weak return types, and APIs that force callers to guess.

### Treat verbosity as a signal to improve boundaries
When typing feels noisy, look for missing concepts such as DTOs, value objects, collections, or named methods. The goal is clearer code, not annotations for their own sake.

## Examples
### Make array shapes explicit at the boundary
Static analysis becomes useful when boundary data has a documented shape.

```php
<?php

/** @return array{name: string, email: string} */
public function validatedData(): array
{
    return $this->validated();
}
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
