# Request objects in Tempest

URL: https://stitcher.io/blog/request-objects-in-tempest
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2025-03-17
Status: curated-processed
Topics: request-data, type-safety, framework-design

## Why This Helps Programming
Shows the same typed-boundary idea from a framework-design angle: the object you actually want should drive request validation and mapping.

## Guidelines
### Design request handling around the target object
Instead of treating arrays as the application interface, define the object your use case needs and map the request into it as early as possible.

### Infer obvious validation from types, then add explicit business rules
Required fields, nullability, scalar types, and enum values can often be derived from type signatures. Keep custom validation for rules the type system cannot express.

## Examples
No concrete code example was added for this article yet.

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
