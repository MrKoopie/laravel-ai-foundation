# PHPStan And Type Safety

## The Short Version
Use static analysis and native types to catch defects before runtime and to give AI tools a stricter contract.

## Practical Rules
- Prefer native type declarations where PHP supports them.
- Use PHPStan or Larastan to check model properties, request data, and return types.
- Raise strictness gradually, but make the configured level non-negotiable in CI.
- Use type coverage to prevent new untyped code from quietly entering the codebase.

## Tips And Tricks
### Catch property mistakes before runtime
Static analysis can detect access to model properties or array keys that do not exist. ([source](../videos/2025-03-25-phpstan-loves-this-trick-strongly-typed-requests-E9ixq-dlcjQ.md))

### Make typed requests visible to tools
Strongly typed form request data makes downstream code easier for PHPStan, humans, and agents to understand. ([source](../videos/2025-03-25-phpstan-loves-this-trick-strongly-typed-requests-E9ixq-dlcjQ.md))

### Treat PHPStan like TypeScript for PHP
Use static analysis as a daily feedback loop, not as an occasional cleanup task. ([source](../articles/stitcher-io/2022-07-16-uncertainty-doubt-and-static-analysis.md))

## Examples
### Typed form request shape
Expose a typed method so callers do not pass unknown arrays around the app.

```php
<?php

final class StoreUserRequest extends FormRequest
{
    /** @return array{name: string, email: string} */
    public function validatedData(): array
    {
        return $this->validated();
    }
}
```

### PHPStan command
Keep analysis easy to run locally and in CI.

```bash
vendor/bin/phpstan analyse --memory-limit=1G
```

## Source Videos
- [AI Vibe Coding Is Broken. Strict Engineering Fixes It.](../videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md)
- [Modern PHP Type Safety with PHPStan..](../videos/2025-10-28-modern-php-type-safety-with-phpstan-rSMi1vJ942o.md)

## Source Articles
- [Tests and types](../articles/stitcher-io/2019-06-07-tests-and-types.md)
- [Uncertainty, doubt, and static analysis](../articles/stitcher-io/2022-07-16-uncertainty-doubt-and-static-analysis.md)
- [What about typed request classes?](../articles/stitcher-io/2021-06-29-what-about-request-classes.md)

## Related Topics
- [AI Engineering Guardrails](ai-engineering.md)
- [Clean Laravel Code](clean-code.md)
- [Testing Strategy](testing.md)
