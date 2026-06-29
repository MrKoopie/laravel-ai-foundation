# Combining event sourcing and stateful systems

URL: https://stitcher.io/blog/combining-event-sourcing-and-stateful-systems
Source: [Stitcher.io](https://stitcher.io/)
Author: Brent
Published: 2020-04-14
Status: curated-processed
Topics: event-sourcing, ddd, architecture

## Why This Helps Programming
Explains that a Laravel application can mix CRUD-style stateful models and event-sourced domains instead of forcing one architecture everywhere.

## Guidelines
### Event source the domains that need it
Use ordinary Eloquent models for simple admin CRUD or low-history data. Use event sourcing where history, reporting, money movement, or workflow reconstruction is central.

### Keep projections disposable
A projection exists to answer reads. It should be rebuildable from events, so do not hide irreversible business writes inside a projector.

## Examples
No concrete code example was added for this article yet.

## Source Notes
- Guidance is paraphrased and synthesized from the source article; full article text is not stored in this repository.
- Use the URL above when the original wording, full context, or comments matter.
