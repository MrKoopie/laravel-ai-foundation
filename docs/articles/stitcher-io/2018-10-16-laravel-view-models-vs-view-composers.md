# Laravel view models vs. view composers

URL: https://stitcher.io/blog/laravel-view-models-vs-view-composers
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2018-10-16
Status: curated-processed
Topics: laravel, frontend, explicit-boundaries

## Why This Helps Programming
Shows why explicit view data is easier to maintain than variables injected through global registration.

## Guidelines
### Prefer explicit view models for complex screens
A view model makes it clear which data a view receives and where it comes from. View composers can be fine for global layout data, but they hide page-specific inputs.

### Make reusable views receive their data intentionally
Create and edit screens can share a form more safely when the controller passes an explicit object instead of relying on ambient variables.

## Examples
No concrete code example was added for this article yet.

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
