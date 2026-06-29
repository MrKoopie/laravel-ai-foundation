# Dealing with dependencies

URL: https://stitcher.io/blog/dealing-with-dependencies
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2022-01-19
Status: curated-processed
Topics: dependencies, maintenance, upgrades

## Why This Helps Programming
Gives an upgrade playbook for external dependencies: test early, contribute fixes, look for alternatives, and fork only as a last resort.

## Guidelines
### Test dependency compatibility before the release day
Start checking against PHP and framework release candidates so incompatibilities are discovered while there is still time to fix them upstream.

### Prefer upstream contribution over local workarounds
If a package blocks an upgrade, first check existing issues and pull requests, then offer a focused fix. Forking transfers maintenance burden to your app and should be a last resort.

## Examples
No concrete code example was added for this article yet.

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
