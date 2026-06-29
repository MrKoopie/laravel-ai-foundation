# Don't be clever

URL: https://stitcher.io/blog/dont-be-clever
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2023-06-02
Status: curated-processed
Topics: clean-code, architecture, maintainability

## Why This Helps Programming
A warning against abstractions that look elegant until real business exceptions start accumulating around them.

## Guidelines
### Do not abstract before the business variation is visible
Generic controllers, repositories, or service layers can hide duplication, but they also hide the places where workflows differ. Wait until the repeated shape and the exceptions are both understood.

### Prefer boring explicit code over clever shared machinery
If a small business exception requires hooks, flags, and override methods, the abstraction is probably costing more than the duplication it removed.

## Examples
No concrete code example was added for this article yet.

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
