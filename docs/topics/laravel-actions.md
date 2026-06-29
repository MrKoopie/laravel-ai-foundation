# Laravel Actions

## The Short Version
Use action classes selectively when named application behavior needs reuse, coordination, transactions, or an invariant-focused test surface.

## Practical Rules
- Before creating an action, ask what pressure justifies it: reuse, multiple entry points, multiple collaborators, a transaction boundary, or a business invariant.
- Keep HTTP concerns out of action classes.
- Validate at the boundary, then pass plain data or DTOs into the action. The reason is that validation is a boundary concern: HTTP requests, queued jobs, console commands, and tests all enter the application differently, while the action should receive trusted, already-shaped input.
- Wrap multi-step mutations in transactions when partial success would corrupt state.
- Do not create an action just to wrap a single obvious Eloquent call.
- Keep simple one-off HTTP-only behavior in the controller until a use-case name, reuse pressure, or business invariant appears.
- Use actions for behavior that needs a name, has more than one entry point, coordinates multiple collaborators, or protects a business rule.

## Tips And Tricks
### Keep controllers thin, not empty by default
Controllers should translate HTTP into application calls. That does not mean every line needs an action; create the action when the behavior has earned a reusable name. ([source](../videos/2026-06-03-the-action-pattern-is-key-to-clean-code-k_gMfdpSXQE.md))

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

### Action boundary after pressure appears
The action receives application data, not an HTTP request. Use this shape after the workflow earns a name or needs reuse.

```php
<?php

declare(strict_types=1);

final readonly class RegisterSubscriber
{
    public function handle(SubscriberData $data): Subscriber
    {
        return DB::transaction(function () use ($data) {
            $subscriber = Subscriber::query()->create($data->toArray());

            SubscribeToDefaultList::dispatchSync($subscriber);

            return $subscriber;
        });
    }
}
```

### Controller calls an action
The controller owns HTTP concerns; the action owns the named workflow that has earned extraction.

```php
<?php

final class RegisterSubscriberController
{
    public function __invoke(RegisterSubscriberRequest $request, RegisterSubscriber $register): RedirectResponse
    {
        $subscriber = $register->handle($request->data());

        return redirect()->route('subscribers.show', $subscriber);
    }
}
```

### Job reuses the same action
Because validation stayed outside the action, a queued job can call it with data that came from another trusted source.

```php
<?php

final readonly class ImportSubscriberJob
{
    public function __construct(private SubscriberData $data) {}

    public function handle(RegisterSubscriber $register): void
    {
        $register->handle($this->data);
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

## Source Articles
- [Don't be clever](../articles/stitcher-io/2023-06-02-dont-be-clever.md)
- [Reducing code motion](../articles/stitcher-io/2025-10-22-reducing-code-motion.md)

## Related Topics
- [Avoid Overengineering](avoid-overengineering.md)
- [Clean Laravel Code](clean-code.md)
- [Database Integrity](database-integrity.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
