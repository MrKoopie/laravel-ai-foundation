# Things dependency injection is not about

URL: https://stitcher.io/blog/things-dependency-injection-is-not-about
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2019-07-30
Status: curated-processed
Topics: dependencies, testing, architecture

## Why This Helps Programming
Clarifies the difference between dependency injection and service location, which matters a lot in Laravel service-container-heavy codebases.

## Guidelines
### Do not use the container as a service locator inside domain code
Calling the container from inside classes hides dependencies and makes tests guess what the object needs. Let Laravel resolve dependencies at the boundary, then pass them explicitly.

### Constructor signatures are documentation
A constructor that names collaborators tells reviewers, static analysis, and tests what the object needs. Hidden container calls erase that information.

## Examples
### Avoid service location in an action
Ask for the dependency once instead of resolving it at the point of use.

```php
<?php

final readonly class PublishPost
{
    public function __construct(private SearchIndexer $indexer) {}

    public function handle(Post $post): void
    {
        $post->publish();
        $this->indexer->index($post);
    }
}
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
