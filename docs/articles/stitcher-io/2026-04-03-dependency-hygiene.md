# Dependency Hygiene

URL: https://stitcher.io/blog/dependency-hygiene
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2026-04-03
Status: curated-processed
Topics: dependencies, security, maintenance

## Why This Helps Programming
Turns package management into an explicit security and maintenance practice, not just `composer require` muscle memory.

## Guidelines
### Audit why every package is installed
Use `composer why` and remove dependencies that are no longer used. Unused packages still expand the code you trust, update, and scan.

### Treat transitive dependencies as part of your system
Package managers make dependency trees easy to ignore. Review high-impact transitive packages, especially around security, crypto, HTTP, file handling, and build tooling.

## Examples
### Dependency audit commands
Small checks make package ownership visible during maintenance.

```bash
composer why symfony/polyfill-mbstring
composer why-not php ^8.4
composer audit
composer outdated --direct
```

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
