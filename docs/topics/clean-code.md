# Clean Laravel Code

## The Short Version
Keep code readable by giving each layer one job: requests validate, controllers orchestrate, actions perform behavior, and tests describe outcomes.

## Practical Rules
- Use strict equality and strict types when possible.
- Move validation to form requests.
- Move reusable behavior to actions or dedicated classes.
- Use DTOs when they clarify boundaries; avoid them when arrays are simpler and well typed.

## Tips And Tricks
### Do not let controllers become workflows
Controllers should be thin enough that the application behavior has a reusable name elsewhere. ([source](../videos/2025-12-26-laravel-clean-code-invokable-controllers-form-requests-jobs-and-more-ZdzdOcdRowk.md))

### Use form requests for validation
A form request gives validation a home and keeps controller methods from turning into input parsing code. ([source](../videos/2025-03-20-laravel-clean-code-how-to-write-perfect-form-requests-FfDu-XR-8YQ.md))

### Prefer strict comparisons
Strict equality avoids PHP coercion surprises and makes intent easier to inspect. ([source](../videos/2025-02-05-always-use-strict-equality-hcI06mTlbzM.md))

## Examples
### Thin invokable controller
One HTTP endpoint, one orchestration path.

```php
<?php

final class PublishPostController
{
    public function __invoke(PublishPostRequest $request, PublishPost $publish): RedirectResponse
    {
        $publish->handle($request->validated());

        return back();
    }
}
```

## Source Videos
- [Laravel Clean Code: Invokable Controllers, Form Requests, Jobs, and More](../videos/2025-12-26-laravel-clean-code-invokable-controllers-form-requests-jobs-and-more-ZdzdOcdRowk.md)
- [Laravel Clean Code: How to Write Perfect Form Requests!](../videos/2025-03-20-laravel-clean-code-how-to-write-perfect-form-requests-FfDu-XR-8YQ.md)
- [Always use STRICT EQUALITY](../videos/2025-02-05-always-use-strict-equality-hcI06mTlbzM.md)

## Source Articles
- [Don't be clever](../articles/stitcher-io/2023-06-02-dont-be-clever.md)
- [Reducing code motion](../articles/stitcher-io/2025-10-22-reducing-code-motion.md)
- [Laravel view models vs. view composers](../articles/stitcher-io/2018-10-16-laravel-view-models-vs-view-composers.md)

## Related Topics
- [Laravel Actions](laravel-actions.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
- [Testing Strategy](testing.md)
