# Dynamic Strategies

URL: https://stitcher.io/blog/strategies
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2022-04-06
Status: curated-processed
Topics: architecture, extensibility, type-safety

## Why This Helps Programming
Explores the strategy pattern from the API consumer's point of view, including how extensibility can weaken type guarantees if the boundary is not designed carefully.

## Guidelines
### Design extension points from the implementer side too
A strategy interface should be pleasant for both the core object and third-party implementations. If implementers need awkward casts or broad mixed inputs, the extension point is leaking complexity.

### Keep strategy inputs as narrow as possible
A strategy receiving `mixed` can support many cases but loses static guarantees. Split strategies or add typed adapters when the behavior has different input families.

## Examples
No concrete code example was added for this article yet.

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
