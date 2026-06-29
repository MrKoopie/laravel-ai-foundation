# Database Integrity

## The Short Version
Protect application state with explicit constraints, transactions, and schema changes that match production behavior.

## Practical Rules
- Use database constraints for invariants the application must never violate.
- Wrap multi-step writes in transactions when partial success would be wrong.
- Prefer migrations over production seeders for production data changes.
- Be cautious with cascade deletes and defaults because they can hide destructive behavior.

## Tips And Tricks
### Use composite unique constraints
Let the database enforce uniqueness when an invariant depends on multiple columns.

### Avoid partial writes
Use transactions around workflows that update multiple records or call external services.

### Do production data changes with migrations
Migrations make production data changes reviewable, ordered, and repeatable.

## Examples
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

## Source Videos
- No source videos have been linked yet.

## Source Articles
- [Unsafe SQL functions in Laravel](../articles/stitcher-io/2019-04-10-unsafe-sql-functions-in-laravel.md)

## Related Topics
- [Laravel Actions](laravel-actions.md)
- [Testing Strategy](testing.md)
