# Examples

Concrete snippets and configurations distilled from the topic guides.

## AI Engineering Guardrails

### Composer quality gate
Use one command for CI and agents. Keep mutation-free checks separate from local fixers.

```json
{
  "scripts": {
    "lint": "pint && rector --dry-run && phpstan analyse",
    "test": "pest --parallel --coverage --min=80",
    "ci": "composer lint && composer test"
  }
}
```

### Agent instruction snippet
Keep instructions short, enforceable, and tied to actual commands.

```md
Before finishing:
- Run `composer ci`.
- Do not mark work complete while tests, static analysis, or formatting fail.
- Follow existing Laravel action, form request, and typed model patterns.
```

## Clean Laravel Code

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

## Database Integrity

### Composite unique constraint
Enforce the invariant where concurrent requests cannot bypass it.

```php
<?php

Schema::table('team_user', function (Blueprint $table) {
    $table->unique(['team_id', 'user_id']);
});
```

### Transactional workflow
Roll back the whole mutation if any step fails.

```php
<?php

DB::transaction(function () use ($data) {
    $order = Order::query()->create($data);
    ReserveInventory::dispatchSync($order);
});
```

## Dependencies And Maintenance

### Dependency maintenance script
Give teams and agents a boring way to inspect package health.

```json
{
  "scripts": {
    "deps:audit": "composer audit && composer outdated --direct",
    "deps:why": "composer why"
  }
}
```

## Developer Tooling

### Repository scripts
Scripts make tool usage discoverable.

```json
{
  "scripts": {
    "format": "pint",
    "analyse": "phpstan analyse",
    "refactor": "rector --dry-run",
    "test": "pest"
  }
}
```

## Domain Modeling In PHP

### Value object plus enum
Types carry business language across actions, jobs, tests, and models.

```php
<?php

final readonly class Percentage
{
    public function __construct(public int $value)
    {
        if ($value < 0 || $value > 100) {
            throw new InvalidArgumentException('Percentage must be between 0 and 100.');
        }
    }
}

enum DiscountType: string
{
    case FIXED = 'fixed';
    case PERCENTAGE = 'percentage';

    public function requiresPercentage(): bool
    {
        return $this === self::PERCENTAGE;
    }
}
```

## Event Sourcing

### Fact event and projection
The event records what happened; the projection answers a read question.

```php
<?php

final readonly class OrderWasPaid
{
    public function __construct(
        public string $orderId,
        public Money $amount,
        public DateTimeImmutable $paidAt,
    ) {}
}

final class OrdersToShipProjector
{
    public function onOrderWasPaid(OrderWasPaid $event): void
    {
        OrdersToShip::query()->create([
            'order_id' => $event->orderId,
            'paid_at' => $event->paidAt,
        ]);
    }
}
```

## Frontend Integration

### Typed page props
Make backend-provided props explicit in frontend code.

```ts
type UserPageProps = {
  user: {
    id: number;
    name: string;
    email: string;
  };
};

export default function ShowUser({ user }: UserPageProps) {
  return <h1>{user.name}</h1>;
}
```

## Laravel Actions

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

## PHPStan And Type Safety

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

## Request Data Boundaries

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

## Testing Strategy

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
