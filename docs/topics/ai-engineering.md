# AI Engineering Guardrails

## The Short Version
Use strict project defaults so AI-generated code is easier to review, test, and trust.

## Practical Rules
- Treat generated code as your responsibility, not as an external artifact.
- Give agents stable commands for linting, testing, static analysis, and coverage.
- Make conventions obvious in the codebase because agents copy nearby patterns.
- Prefer automated checks over prose instructions when a rule can be enforced.

## Tips And Tricks
### Use types as the first guardrail
Run PHPStan for PHP and TypeScript for frontend code so generated mistakes are caught across the project. ([source](../videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md))

### Hide checks behind stable commands
Expose commands such as `composer lint` and `composer test` so humans, agents, and CI all run the same quality pipeline. ([source](../videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md))

### Write repo-level AI instructions
Tell agents which commands to run, which conventions to follow, and when work is not complete yet. ([source](../videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md))

## Examples
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

## Source Videos
- [AI Vibe Coding Is Broken. Strict Engineering Fixes It.](../videos/2026-05-27-ai-vibe-coding-is-broken-strict-engineering-fixes-it-96To5-uJbog.md)
- [How I Code With AI Right Now](../videos/2026-05-31-how-i-code-with-ai-right-now-heAVDeRZiUA.md)
- [AI Vibe Coding Just Got 10x Better (With Rules Files)](../videos/2025-03-24-ai-vibe-coding-just-got-10x-better-with-rules-files-Hi6zlum3K2k.md)

## Related Topics
- [Testing Strategy](testing.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
- [Developer Tooling](tooling.md)
