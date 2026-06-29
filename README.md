# Programming Foundation

This repository turns programming-useful videos and articles into searchable Markdown notes and topic guides. The first video source is [nunomaduro](https://www.youtube.com/@nunomaduro), and the first blog source is [Stitcher.io](https://stitcher.io/).

Start with [docs/indexes/topics.md](docs/indexes/topics.md). The topic guides in [docs/topics](docs/topics) synthesize tips across multiple videos and include examples. Individual notes in [docs/videos](docs/videos) remain as source/provenance pages.

The archive tracks every public upload in [videos.md](videos.md). Videos that do not contain reusable programming advice are marked as skipped. Programming-useful videos get individual notes in [docs/videos](docs/videos), and the source-video topic map lives in [docs/indexes/video-topics.md](docs/indexes/video-topics.md).

Curated blog articles get individual notes in [docs/articles](docs/articles), and the blog source index lives in [docs/indexes/blog-sources.md](docs/indexes/blog-sources.md). Article notes paraphrase and synthesize the guidance; full article bodies are not copied into the repository.

## Context7

The root [context7.json](context7.json) tells Context7 to index the Markdown documentation in `docs/` while ignoring source metadata and helper scripts. For search, prefer `docs/topics` and `docs/examples`; use `docs/videos` to trace a tip back to its source video.

To add this repo to Context7, publish it on GitHub and add the repository URL through Context7's GitHub import flow.

## Laravel Boost

The repository includes [boost.json](boost.json), [AGENTS.md](AGENTS.md), and [.ai/guidelines/programming-foundation.md](.ai/guidelines/programming-foundation.md) so Boost-compatible agents can understand how to work with the archive.

This is a Markdown documentation repository, not a Laravel application, so Boost runtime features such as MCP, Sail, Nightwatch, and Laravel Cloud are disabled in `boost.json`. The compatible surface is project guidance: agents should preserve the generated-doc workflow, prioritize topic guides for search, and keep only genuinely programming-useful tips.

`boost.json` lists every agent currently supported by Laravel Boost: Amp, Junie, Cursor, Claude Code, Codex, Copilot, Factory, Kiro, OpenCode, Antigravity, Zed, and Pi. Boost uses [CLAUDE.md](CLAUDE.md) for Claude Code and [AGENTS.md](AGENTS.md) for the other supported agents.

## Agent Skill

The repo includes a repo-local Codex plugin at [plugins/laravel-ai-foundation](plugins/laravel-ai-foundation). Its skill tells agents to query the live Context7 library `/mrkoopie/laravel-ai-foundation` before making Laravel architecture decisions, especially around actions, request boundaries, DDD, testing, and avoiding overengineering.

The portable skill file is [plugins/laravel-ai-foundation/skills/laravel-ai-foundation/SKILL.md](plugins/laravel-ai-foundation/skills/laravel-ai-foundation/SKILL.md). Codex can use it through the plugin marketplace manifest in [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json); Claude/Claude Code can reuse the same `SKILL.md` content as a normal skill.

## Source Data

The source metadata and captions used for analysis are kept in [data/source](data/source). YouTube sources are grouped by channel under [data/source/channels](data/source/channels). Blog sources are grouped under [data/source/blogs](data/source/blogs).

The current YouTube source snapshot lives in [data/source/channels/nunomaduro](data/source/channels/nunomaduro) and includes the raw `yt-dlp` metadata snapshot, generated metadata with processing status, selected programming URLs, and raw YouTube JSON3 caption files.

The current blog source snapshot lives in [data/source/blogs/stitcher-io](data/source/blogs/stitcher-io) and includes the fetched RSS snapshot, raw article metadata, enriched processing status, and the curated article index.

## Updating The Archive

The checked-in helper scripts keep generation repeatable:

```bash
python3 -m pip install yt-dlp
python3 -m yt_dlp --skip-download --print '%(.{id,title,upload_date,duration,duration_string,webpage_url,description})j' 'https://www.youtube.com/@nunomaduro/videos' > /tmp/nunomaduro-videos.jsonl
python3 -m tools.render_archive --metadata /tmp/nunomaduro-videos.jsonl --repo .
```

To rerender from the checked-in source snapshot:

```bash
python3 -m tools.render_archive \
  --metadata data/source/channels/nunomaduro/youtube-videos.raw.jsonl \
  --captions data/source/channels/nunomaduro/captions/youtube-json3 \
  --channel-slug nunomaduro \
  --repo .
```

Caption-derived notes can be improved by refreshing captions into a temporary directory and passing `--captions`.

To rerender the Stitcher.io blog source from a fresh RSS snapshot:

```bash
curl -L -o /tmp/stitcher-rss.xml https://stitcher.io/rss
python3 -m tools.render_blog_archive \
  --source stitcher-io \
  --rss /tmp/stitcher-rss.xml \
  --repo .
```
