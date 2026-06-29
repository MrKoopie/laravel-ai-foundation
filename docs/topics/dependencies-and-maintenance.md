# Dependencies And Maintenance

## The Short Version
Keep collaborators, packages, and upgrade work explicit so the codebase stays understandable and safe to evolve.

## Practical Rules
- Inject collaborators instead of locating them from the container inside domain or action code.
- Audit why packages are installed and remove unused dependencies.
- Treat deprecations as early upgrade work, not as ignorable noise.
- Contribute upstream fixes before forking dependencies.

## Tips And Tricks
### Avoid service location in application code
Resolving dependencies from the container inside a class hides what the class needs. Constructor injection makes dependencies visible to tests, reviewers, and static analysis. ([source](../articles/stitcher-io/2019-07-30-things-dependency-injection-is-not-about.md))

### Use package hygiene commands regularly
`composer why`, `composer audit`, and `composer outdated --direct` help you understand the code you trust and whether it is still needed. ([source](../articles/stitcher-io/2026-04-03-dependency-hygiene.md))

### Turn deprecations into a rolling backlog
Deprecations are future failures with a grace period. Fix them in small batches while the application still runs. ([source](../articles/stitcher-io/2022-05-18-dealing-with-deprecations.md))

## Examples
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

## Source Videos
- [Important Composer Security Update](../videos/2026-05-30-important-composer-security-update-vebiqijeswQ.md)

## Source Articles
- [Dependency injection for beginners](../articles/stitcher-io/2018-04-30-dependency-injection-for-beginners.md)
- [Things dependency injection is not about](../articles/stitcher-io/2019-07-30-things-dependency-injection-is-not-about.md)
- [Dealing with dependencies](../articles/stitcher-io/2022-01-19-dealing-with-dependencies.md)
- [Dependency Hygiene](../articles/stitcher-io/2026-04-03-dependency-hygiene.md)
- [Dealing with deprecations](../articles/stitcher-io/2022-05-18-dealing-with-deprecations.md)

## Related Topics
- [Developer Tooling](tooling.md)
- [Testing Strategy](testing.md)
- [Clean Laravel Code](clean-code.md)
