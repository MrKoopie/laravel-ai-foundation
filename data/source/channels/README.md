# Source Channels

Each YouTube channel gets its own source folder:

```text
data/source/channels/<channel-slug>/
  channel.json
  README.md
  youtube-videos.raw.jsonl
  videos.jsonl
  programming-video-urls.txt
  captions/
    youtube-json3/
```

Use the YouTube handle without `@` as the default slug, lowercased when possible. For example, `@nunomaduro` is stored in `nunomaduro`.

## Current Channels

- [nunomaduro](nunomaduro/README.md)
