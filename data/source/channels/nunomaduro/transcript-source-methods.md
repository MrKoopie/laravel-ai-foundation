# Transcript Source Methods

Channel: [@nunomaduro](https://www.youtube.com/@nunomaduro)
Checked: 2026-06-29

## Validated Example

Video: [Digging Into Laravel Breeze's Livewire Stack: Starter Kits Options [Part 1/5]](https://www.youtube.com/watch?v=GMUkj23bznA)

`GMUkj23bznA` has an English YouTube automatic-caption track. The repository already stores it as:

```text
data/source/channels/nunomaduro/captions/youtube-json3/GMUkj23bznA.en.json3
```

Parsing that JSON3 caption file produces about 9k characters of transcript text.

## Ways To Retrieve The Same Transcript

### 1. Existing Repository Caption Source

Use the checked-in JSON3 file when it exists. This is the preferred source because it is reproducible and does not depend on a live third-party page.

### 2. yt-dlp Automatic Captions

`yt-dlp --list-subs` reports automatic captions for `GMUkj23bznA`, including English and `json3` format. It reports no manual subtitles for this video.

Reusable command:

```bash
PYTHONPATH=/private/tmp/codex-ytdlp python3 -m yt_dlp \
  --skip-download \
  --write-auto-subs \
  --sub-langs en \
  --sub-format json3 \
  'https://www.youtube.com/watch?v=GMUkj23bznA'
```

### 3. YouTube Timedtext Endpoint

`yt-dlp` exposes a signed YouTube `api/timedtext` URL for the requested caption track. This can retrieve the same auto-caption data, but the URL contains temporary parameters and should not be stored as a durable source.

### 4. Third-Party Transcript Pages

The page `https://youtubetotranscript.com/transcript?v=GMUkj23bznA` can show a transcript in a browser, but automated access from this environment returned a Cloudflare challenge instead of transcript content. Treat this kind of site as a convenience UI over YouTube caption data, not as a separate source of truth.

## What This Means For Missing Transcripts

For videos where YouTube exposes neither manual subtitles nor automatic captions, third-party transcript pages may still fail unless they run their own speech-to-text. The reliable fallback for this repository is still ASR from audio, stored under:

```text
data/source/channels/nunomaduro/transcripts/asr/<video-id>.md
```
