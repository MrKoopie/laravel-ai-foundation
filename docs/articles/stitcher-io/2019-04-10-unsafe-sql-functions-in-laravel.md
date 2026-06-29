# Unsafe SQL functions in Laravel

URL: https://stitcher.io/blog/unsafe-sql-functions-in-laravel
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2019-04-10
Status: curated-processed
Topics: laravel, security, database

## Why This Helps Programming
A concrete Laravel reminder that framework helpers do not make user-controlled column names or raw SQL fragments safe by default.

## Guidelines
### Whitelist user-selectable columns
Never let request input directly choose SQL columns, JSON paths, `orderBy` fields, or select expressions. Map public filter names to known internal columns.

### Prefer framework-safe syntax over raw fragments
Use Laravel's supported JSON selector syntax and query builder APIs where possible, but still validate which fields the user is allowed to address.

## Examples
### Whitelist sortable fields
Map request values to known columns before passing them to the query builder.

```php
<?php

$sort = $request->string('sort')->toString();

$column = [
    'name' => 'users.name',
    'created' => 'users.created_at',
][$sort] ?? 'users.created_at';

User::query()->orderBy($column)->get();
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
