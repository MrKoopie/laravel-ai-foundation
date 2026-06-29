# What about typed request classes?

URL: https://stitcher.io/blog/what-about-request-classes
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2021-06-29
Status: curated-processed
Topics: request-data, laravel, type-safety

## Why This Helps Programming
Explores the gap between Laravel validation arrays and typed request data that IDEs, static analysis, and application services can understand.

## Guidelines
### Separate raw request validation from trusted application data
A form request is excellent at validating HTTP input, but the rest of the application benefits from a typed representation. Convert boundary arrays into a DTO or typed method before calling actions.

### Make validation rules visible to tools where practical
String validation rules are easy for Laravel to run, but hard for PHPStan and IDEs to understand. Add typed accessors, DTOs, or dedicated data objects when the data crosses into reusable application code.

## Examples
### Request to data object
The controller converts HTTP input into typed data before calling the use case.

```php
<?php

final readonly class UpdatePostData
{
    public function __construct(
        public string $title,
        public PostStatus $status,
        public string $body,
    ) {}
}

final class UpdatePostRequest extends FormRequest
{
    public function data(): UpdatePostData
    {
        $validated = $this->validated();

        return new UpdatePostData(
            title: $validated['title'],
            status: PostStatus::from($validated['status']),
            body: $validated['body'],
        );
    }
}
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
