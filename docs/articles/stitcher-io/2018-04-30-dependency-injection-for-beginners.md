# Dependency injection for beginners

URL: https://stitcher.io/blog/dependency-injection-for-beginners
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2018-04-30
Status: curated-processed
Topics: dependencies, architecture, object-design

## Why This Helps Programming
Explains dependency injection as composition: objects receive collaborators instead of constructing or locating everything themselves.

## Guidelines
### Compose behavior from collaborators
Prefer giving an object the collaborator it needs over hard-coding concrete construction inside it. This makes variation explicit and testing simpler.

### Do not inject every scalar or incidental value
Dependency injection is for services and collaborators. Runtime data should usually be method input or a value object.

## Examples
### Inject the collaborator, pass runtime data
The mailer is a dependency; the email address is input.

```php
<?php

final readonly class InviteUser
{
    public function __construct(private Mailer $mailer) {}

    public function handle(EmailAddress $email): void
    {
        $this->mailer->send(new InvitationMail($email));
    }
}
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
