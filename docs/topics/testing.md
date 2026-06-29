# Testing Strategy

## The Short Version
Use fast, focused tests plus coverage and quality gates so code changes are safe to accept.

## Practical Rules
- Start with smoke tests for broad confidence, then add focused tests for risky behavior.
- Prefer arrange-act-assert structure so test intent is obvious.
- Avoid mocks when a real collaborator gives better confidence at acceptable cost.
- Run tests in parallel when suite time would discourage frequent checks.

## Tips And Tricks
### Make the first test a smoke test
A smoke test proves the critical path still works before you spend time on smaller cases. ([source](../videos/2025-01-06-why-smoke-tests-should-always-be-your-first-test-6iz1uPS-s3A.md))

### Keep test shape readable
Arrange-act-assert keeps setup, behavior, and expectations separate. ([source](../videos/2024-12-03-clean-tests-with-arrange-act-assert-bBZ44BeDVTg.md))

### Use coverage as a guardrail
Coverage thresholds are most useful when they prevent AI-generated code from shipping without tests. ([source](../videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md))

## Examples
### Arrange-act-assert test
Make the test read as a tiny story.

```php
<?php

it('creates a user from valid input', function () {
    $data = User::factory()->raw();

    $user = app(CreateUser::class)->handle($data);

    expect($user)->email->toBe($data['email']);
});
```

### Parallel coverage gate
Fast checks are easier to run often.

```bash
vendor/bin/pest --parallel --coverage --min=80
```

## Source Videos
- [Your PHP Tests Are Not Enough in 2026](../videos/2026-05-26-your-php-tests-are-not-enough-in-2026-WhXf_mM5k7c.md)
- [3 testing tips you need to know...](../videos/2024-12-19-3-testing-tips-you-need-to-know-shgXQUkCixw.md)
- [Why Smoke Tests Should Always Be Your First Test](../videos/2025-01-06-why-smoke-tests-should-always-be-your-first-test-6iz1uPS-s3A.md)

## Source Articles
- [Testing Patterns](../articles/stitcher-io/2024-03-22-testing-patterns.md)
- [Tests and types](../articles/stitcher-io/2019-06-07-tests-and-types.md)

## Related Topics
- [AI Engineering Guardrails](ai-engineering.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
- [Developer Tooling](tooling.md)
