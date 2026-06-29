# Request Data Boundaries

## The Short Version
Validate raw input at the edge, then pass typed, trusted data into application behavior.

## Practical Rules
- Treat HTTP request objects as boundary objects, not application-service input.
- Convert validated request data into a DTO, typed accessor, or value object before calling reusable actions.
- Let types express required fields, nullability, enums, and simple scalar expectations where practical.
- Keep custom validation for rules the type system cannot express.

## Tips And Tricks
### Make application input visible to tools
Validated arrays are easy for Laravel, but weak for static analysis. A typed request method or DTO tells IDEs, PHPStan, tests, and reviewers what the action receives. ([source](../articles/stitcher-io/2021-06-29-what-about-request-classes.md))

### Design around the object the use case needs
The rest of the application usually wants a typed object, not an HTTP request. Build the boundary so the controller maps raw input into that object early. ([source](../articles/stitcher-io/2025-03-17-request-objects-in-tempest.md))

### Keep validation outside reusable actions
Validation belongs at the entry boundary because web requests, jobs, CLI commands, imports, and tests all enter the application differently. The action should receive already-shaped data and enforce behavior-specific invariants. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

## Examples
### Typed request data before the action
The request owns HTTP validation; the action receives application data.

```php
<?php

final readonly class StorePostData
{
    public function __construct(
        public string $title,
        public PostStatus $status,
        public string $body,
    ) {}
}

final class StorePostRequest extends FormRequest
{
    public function data(): StorePostData
    {
        $validated = $this->validated();

        return new StorePostData(
            title: $validated['title'],
            status: PostStatus::from($validated['status']),
            body: $validated['body'],
        );
    }
}

final class StorePostController
{
    public function __invoke(StorePostRequest $request, StorePost $storePost): RedirectResponse
    {
        $post = $storePost->handle($request->data());

        return redirect()->route('posts.show', $post);
    }
}
```

## Source Videos
- [The Action Pattern Is Key to Clean Code](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md)

## Source Articles
- [What about typed request classes?](../articles/stitcher-io/2021-06-29-what-about-request-classes.md)
- [Request objects in Tempest](../articles/stitcher-io/2025-03-17-request-objects-in-tempest.md)

## Related Topics
- [Laravel Actions](laravel-actions.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
- [Domain Modeling In PHP](domain-modeling.md)
