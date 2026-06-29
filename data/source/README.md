# Source Data

This directory keeps the source material used to build and re-analyze the archive.

Sources are grouped by source type. YouTube uploads live under [channels](channels), and written sources live under [blogs](blogs). This keeps multiple channels and blogs from sharing one flat source directory as the archive grows.

## Channel Layout

Each channel folder uses the same structure:

```text
data/source/channels/<channel-slug>/
  channel.json
  README.md
  youtube-videos.raw.jsonl
  videos.jsonl
  programming-video-urls.txt
  captions/
    youtube-json3/
  transcript-audit.md
  transcripts/
    asr/
  visual-reviews/
```

See [channels/nunomaduro](channels/nunomaduro/README.md) for the current source snapshot.

## Blog Layout

Each blog folder uses the same structure:

```text
data/source/blogs/<blog-slug>/
  source.json
  README.md
  rss.raw.xml
  articles.raw.jsonl
  articles.jsonl
  articles.md
```

See [blogs/stitcher-io](blogs/stitcher-io/README.md) for the current Stitcher.io source snapshot.

## Re-analysis

To regenerate the archive from repo-owned sources:

```bash
python3 -m tools.render_archive \
  --metadata data/source/channels/nunomaduro/youtube-videos.raw.jsonl \
  --captions data/source/channels/nunomaduro/captions/youtube-json3 \
  --channel-slug nunomaduro \
  --repo .
```

The raw captions are kept as source data. Generated Markdown should still be edited through `tools/archive_tools.py` and `tools/topic_guides.py`, then rerendered.
Blog source metadata is kept for traceability, but full article bodies are not copied into the repository. Generated article notes should be edited through `tools/blog_archive.py` and rerendered with `tools.render_blog_archive`.
