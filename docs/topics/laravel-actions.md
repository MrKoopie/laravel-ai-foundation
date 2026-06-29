# Laravel Actions

## The Short Version
Move reusable application behavior into action classes so controllers, jobs, commands, and other actions can share it.

## Practical Rules
- Keep HTTP concerns out of action classes.
- Validate at the boundary, then pass plain data or DTOs into the action. The reason is that validation is a boundary concern: HTTP requests, queued jobs, console commands, and tests all enter the application differently, while the action should receive trusted, already-shaped input.
- Wrap multi-step mutations in transactions when partial success would corrupt state.
- Do not create an action just to wrap a single obvious Eloquent call.
- Keep simple one-off HTTP-only behavior in the controller until a use-case name, reuse pressure, or business invariant appears.
- Use actions for behavior that needs a name, has more than one entry point, coordinates multiple collaborators, or protects a business rule.

## Tips And Tricks
### Keep controllers thin
Controllers should translate HTTP into application calls; actions should hold the behavior. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

### Pass validated data
Call `validated()` on a form request and pass that result into the action instead of passing the request object. This keeps malformed user input, redirect behavior, authorization messages, and other HTTP-only concerns at the edge of the system. The action can then focus on the business operation and can be reused from non-HTTP entry points without pretending a request exists. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

### Reuse behavior across entry points
The same action can be called from a controller, console command, queued job, or another action. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

### Do not action all the things
An action is useful when behavior has a clear use-case name, more than one entry point, multiple collaborators, a transaction boundary, or a business rule worth testing. A one-line create/update that is only used by one controller can stay inline until the code shows pressure. ([source](../articles/stitcher-io/2023-06-02-dont-be-clever.md))

### Avoid Action per model method
Do not create `CreateUserAction`, `UpdateUserAction`, `DeleteUserAction`, and `FindUserAction` simply because a `User` model exists. That hides ordinary CRUD behind ceremony and teaches agents to route every change through an action. Name actions after real application behavior, such as `InviteTeamMember` or `PublishPost`. ([source](../articles/stitcher-io/2025-10-22-reducing-code-motion.md))

## Examples
### Inline simple CRUD
A single validated write with no reuse and no extra business rule can stay in the controller. This is less ceremony, not less architecture.

```php
<?php

final class StoreTagController
{
    public function __invoke(StoreTagRequest $request): RedirectResponse
    {
        $tag = Tag::query()->create($request->validated());

        return redirect()->route('tags.show', $tag);
    }
}
```

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

### Action-worthy workflow
Create an action when the behavior coordinates several steps or protects a rule that deserves a named test surface.

```php
<?php

final readonly class InviteTeamMember
{
    public function __construct(private Mailer $mailer) {}

    public function handle(Team $team, User $invitedBy, string $email): Invitation
    {
        return DB::transaction(function () use ($team, $invitedBy, $email) {
            $invitation = $team->invitations()->create([
                'email' => $email,
                'invited_by_id' => $invitedBy->id,
            ]);

            $this->mailer->send(new TeamInvitationMail($invitation));

            return $invitation;
        });
    }
}
```

## Source Videos
- [The Action Pattern Is Key to Clean Code](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md)
- [Laravel Actions: The Secret Sauce](../videos/2024-12-02-laravel-actions-the-secret-sauce-r1480BoFulQ.md)
- [Clean Laravel Controllers with Actions and Form Requests](../videos/2025-01-29-clean-laravel-controllers-with-actions-and-form-requests-nLNdQ9q_RxA.md)

## Source Articles
- [Don't be clever](../articles/stitcher-io/2023-06-02-dont-be-clever.md)
- [Reducing code motion](../articles/stitcher-io/2025-10-22-reducing-code-motion.md)

## Related Topics
- [Avoid Overengineering](avoid-overengineering.md)
- [Clean Laravel Code](clean-code.md)
- [Database Integrity](database-integrity.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
