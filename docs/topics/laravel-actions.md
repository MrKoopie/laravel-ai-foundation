# Laravel Actions

## The Short Version
Move reusable application behavior into action classes so controllers, jobs, commands, and other actions can share it.

## Practical Rules
- Keep HTTP concerns out of action classes.
- Validate at the boundary, then pass plain data or DTOs into the action. The reason is that validation is a boundary concern: HTTP requests, queued jobs, console commands, and tests all enter the application differently, while the action should receive trusted, already-shaped input.
- Wrap multi-step mutations in transactions when partial success would corrupt state.
- Use actions for behavior that needs a name and may be reused from multiple entry points.

## Tips And Tricks
### Keep controllers thin
Controllers should translate HTTP into application calls; actions should hold the behavior. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

### Pass validated data
Call `validated()` on a form request and pass that result into the action instead of passing the request object. This keeps malformed user input, redirect behavior, authorization messages, and other HTTP-only concerns at the edge of the system. The action can then focus on the business operation and can be reused from non-HTTP entry points without pretending a request exists. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

### Reuse behavior across entry points
The same action can be called from a controller, console command, queued job, or another action. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

## Examples
### Action class boundary
The action receives application data, not an HTTP request.

```php
<?php

declare(strict_types=1);

final readonly class CreateUser
{
    public function handle(array $data): User
    {
        return DB::transaction(fn () => User::query()->create($data));
    }
}
```

### Controller calls an action
The controller owns HTTP concerns; the action owns behavior.

```php
<?php

final class StoreUserController
{
    public function __invoke(StoreUserRequest $request, CreateUser $createUser): RedirectResponse
    {
        $user = $createUser->handle($request->validated());

        return redirect()->route('users.show', $user);
    }
}
```

### Job reuses the same action
Because validation stayed outside the action, a queued job can call it with data that came from another trusted source.

```php
<?php

final readonly class ImportUserJob
{
    public function __construct(private array $row) {}

    public function handle(CreateUser $createUser): void
    {
        $createUser->handle([
            'name' => $this->row['name'],
            'email' => $this->row['email'],
        ]);
    }
}
```

## Source Videos
- [The Action Pattern Is Key to Clean Code](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md)
- [Laravel Actions: The Secret Sauce](../videos/2024-12-02-laravel-actions-the-secret-sauce-r1480BoFulQ.md)
- [Clean Laravel Controllers with Actions and Form Requests](../videos/2025-01-29-clean-laravel-controllers-with-actions-and-form-requests-nLNdQ9q_RxA.md)

## Related Topics
- [Clean Laravel Code](clean-code.md)
- [Database Integrity](database-integrity.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
