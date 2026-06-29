# nunomaduro Source Snapshot

Channel: [@nunomaduro](https://www.youtube.com/@nunomaduro)

This folder contains the source material used to build and re-analyze the current nunomaduro archive.

## Files

- `channel.json` describes this source channel and its artifact layout.
- `youtube-videos.raw.jsonl` is the raw `yt-dlp` metadata snapshot for all public uploads captured during collection.
- `videos.jsonl` is the enriched metadata written by the archive renderer, including processing status and note paths.
- `programming-video-urls.txt` lists the selected programming-useful video URLs.
- `captions/youtube-json3/` contains the downloaded English YouTube caption JSON3 files used for transcript-derived analysis.
- `transcript-audit.md` records videos where YouTube did not expose captions and identifies the fallback path.
- `transcript-source-methods.md` records validated ways to retrieve transcript data and how they relate to the checked-in caption files.
- `transcripts/` is reserved for generated ASR transcripts when captions are not available.
- `visual-reviews/` contains source notes for silent or near-silent videos processed by inspecting the video frames.

## Re-analysis

```bash
python3 -m tools.render_archive \
  --metadata data/source/channels/nunomaduro/youtube-videos.raw.jsonl \
  --captions data/source/channels/nunomaduro/captions/youtube-json3 \
  --channel-slug nunomaduro \
  --repo .
```

Generated Markdown still lives in the shared `docs/` tree so Context7 can search across channels by topic.
