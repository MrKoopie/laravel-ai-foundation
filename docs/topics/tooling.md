# Developer Tooling

## The Short Version
Make quality tools easy to run, easy to automate, and boring enough that the team actually uses them.

## Practical Rules
- Put repeated tool commands behind scripts.
- Use formatting and static analysis as part of the normal development loop.
- Document repo conventions in config files, not only in memory.
- Adopt upgrade tools when they reduce risky manual work.

## Tips And Tricks
### Use Composer scripts as the stable interface
A single script can hide Pint, Rector, PHPStan, Pest, or other tools behind one command. ([source](../videos/2026-05-26-your-php-tests-are-not-enough-in-2026-WhXf_mM5k7c.md))

### Keep repo config explicit
Files such as `.editorconfig`, `.gitattributes`, and `.gitignore` teach both humans and tools how the project behaves.

### Use Rector for repeatable upgrades
Automated refactors reduce manual migration risk when modernizing PHP or Laravel code. ([source](../videos/2025-10-10-rector-php-for-laravel-is-actually-insane-pmWUDBoFKhs.md))

## Examples
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

## Source Videos
- [Rector PHP For Laravel is ACTUALLY INSANE](../videos/2025-10-10-rector-php-for-laravel-is-actually-insane-pmWUDBoFKhs.md)

## Source Articles
- [Dealing with deprecations](../articles/stitcher-io/2022-05-18-dealing-with-deprecations.md)
- [Dependency Hygiene](../articles/stitcher-io/2026-04-03-dependency-hygiene.md)

## Related Topics
- [AI Engineering Guardrails](ai-engineering.md)
- [Testing Strategy](testing.md)
- [PHPStan And Type Safety](phpstan-type-safety.md)
