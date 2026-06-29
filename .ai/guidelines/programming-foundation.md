# Programming Foundation Guidelines

Use these guidelines when working on the Programming Foundation knowledge base.

## Purpose

This repository turns programming-useful videos and articles into searchable Markdown documentation. The value is in synthesis: topic guides should explain what to do, why it helps, when to apply it, and where the source came from.

## Search Surface

- Prefer `docs/topics/` for direct answers.
- Use `docs/examples/` when the user asks for concrete snippets.
- Use `docs/videos/` to trace a claim back to an individual video.
- Use `docs/articles/` to trace a claim back to an individual article.
- Use `videos.md` only for processing state and coverage checks.

## Content Rules

- Keep programming usefulness as the filter. Skip general career commentary, channel updates, and broad opinions unless they contain an actionable programming practice.
- Do not summarize whole transcripts. Extract durable tips and explain the engineering reason behind each one.
- Preserve source URLs and upload dates in per-video notes.
- Preserve source article URLs and publication dates in per-article notes.
- Prefer paraphrase over quotation.
- Avoid official-sounding claims when a note is advice from a video or article rather than framework documentation.

## Maintenance Rules

- Treat generated Markdown as output. Prefer editing `tools/topic_guides.py`, `tools/archive_tools.py`, or `tools/blog_archive.py`, then rerendering.
- Add tests for repository-structure expectations when adding new metadata formats.
- Keep Context7 focused on end-user documentation by indexing `docs/` rather than source metadata or generator internals.
