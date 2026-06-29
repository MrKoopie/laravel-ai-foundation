# Stitcher.io Source Snapshot

This folder contains the source metadata used to distill programming guidelines from [Stitcher.io](https://stitcher.io/).

- Articles discovered from RSS: 272
- Curated into local notes: 21
- Programming candidates not yet distilled: 141
- Skipped: 110

## Files

- `source.json` describes the source.
- `rss.raw.xml` is the fetched RSS snapshot used for this crawl.
- `articles.raw.jsonl` stores RSS article metadata.
- `articles.jsonl` stores enriched processing status and note paths.
- `articles.md` is the human-readable processing index.

Full article bodies are not copied into the repository. Curated notes in `docs/articles/stitcher-io` link back to the original article and paraphrase the extracted guidance.

## Regeneration

```bash
curl -L -o /tmp/stitcher-rss.xml https://stitcher.io/rss
python3 -m tools.render_blog_archive --source stitcher-io --rss /tmp/stitcher-rss.xml --repo .
```
