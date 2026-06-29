# Repository Instructions

This repository is a generated Markdown knowledge base for programming-useful tips from videos and blogs. Optimize changes for searchable documentation, traceable sources, and concise programming value.

## Project Shape

- `docs/topics/` contains synthesized topic guides and should be the preferred answer surface for search.
- `docs/examples/` contains concrete examples extracted from the topic guides.
- `docs/videos/` contains per-video source notes and provenance.
- `docs/articles/` contains per-article source notes and provenance.
- `videos.md` tracks every channel upload and processing status.
- `data/source/channels/<channel-slug>/` contains raw and enriched source metadata for each YouTube channel.
- `data/source/blogs/<blog-slug>/` contains raw and enriched source metadata for each written source.
- `tools/` contains the generators; generated Markdown should normally be changed by updating the generator and rerendering.

## Content Standards

- Keep only programming videos and tips that genuinely help programming practice.
- Prefer specific, reusable advice over transcript-like summaries.
- Explain the reason behind a recommendation, especially when the rule changes where code should live.
- Include concrete examples where they make a tip easier to apply.
- Include source video URLs, but do not store video media or quote transcripts verbatim.
- Include source article URLs, but do not store full article bodies or quote articles at length.

## Generated Documentation Workflow

- Add or refine synthesis in `tools/topic_guides.py`.
- Add per-video manual overrides in `tools/archive_tools.py` when captions need human interpretation.
- Add per-article curated guidance in `tools/blog_archive.py` when written sources need human interpretation.
- Regenerate with `python3 -m tools.render_archive --metadata <metadata.jsonl> --captions <captions-dir> --channel-slug <channel-slug> --repo .` when captions are available.
- Regenerate blog sources with `python3 -m tools.render_blog_archive --source <blog-slug> --rss <rss.xml> --repo .`.
- Run `python3 -m unittest discover -s tests` after generator or documentation-structure changes.

## Boost Compatibility

- `boost.json` declares this repository as Boost-guideline aware.
- `.ai/guidelines/programming-foundation.md` contains reusable project guidance for Boost-compatible agents.
- This is not a Laravel application, so Boost MCP/runtime features are intentionally disabled in `boost.json`.
