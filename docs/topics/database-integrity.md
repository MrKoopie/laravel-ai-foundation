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
Let the database enforce uniqueness when an invariant depends on multiple columns. ([source](../videos/2025-01-21-keep-your-db-in-check-with-composite-unique-constraints-yT4euHDveVc.md))

### Avoid partial writes
Use transactions around workflows that update multiple records or call external services. ([source](../videos/2025-01-28-avoid-this-mistake-in-your-laravel-db-transactions-N0jlh912xcM.md))

### Do production data changes with migrations
Migrations make production data changes reviewable, ordered, and repeatable. ([source](../videos/2025-02-28-using-laravel-seeders-in-production-stop-use-migrations-instead-HNgDhZYg3VI.md))

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
- [AVOID This Mistake in Your Laravel DB Transactions](../videos/2025-01-28-avoid-this-mistake-in-your-laravel-db-transactions-N0jlh912xcM.md)
- [Keep Your DB in Check with Composite Unique Constraints!](../videos/2025-01-21-keep-your-db-in-check-with-composite-unique-constraints-yT4euHDveVc.md)
- [Using Laravel Seeders in Production? STOP! Use Migrations Instead!](../videos/2025-02-28-using-laravel-seeders-in-production-stop-use-migrations-instead-HNgDhZYg3VI.md)

## Source Articles
- [Unsafe SQL functions in Laravel](../articles/stitcher-io/2019-04-10-unsafe-sql-functions-in-laravel.md)

## Related Topics
- [Laravel Actions](laravel-actions.md)
- [Testing Strategy](testing.md)
