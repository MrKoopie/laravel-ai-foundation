# Transcript Availability Audit

Channel: [@nunomaduro](https://www.youtube.com/@nunomaduro)
Checked: 2026-06-29

## Scope

This audit covers videos in `videos.jsonl` with `archive_status` set to `needs-transcript-review`.

## Result

YouTube does not expose manual subtitles or automatic captions for these videos through the safe `yt-dlp` checks used here. The videos still expose audio streams, but ASR did not produce reliable speech transcripts. They were processed through visual review instead.

For videos that do have YouTube automatic captions, see [transcript-source-methods.md](transcript-source-methods.md). Third-party transcript pages can be useful as a browser UI, but they should not be treated as a separate durable source unless they provide transcript data that is not available through YouTube captions.

| Video ID | Upload Date | Title | Duration | YouTube Subtitles | YouTube Automatic Captions | Audio Available | Recommended Next Step |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `UQ6JrEsyvvw` | 2019-09-18 | PHP Plus - Installation process and class methods | 39s | none | none | yes, format `251` / opus | ASR empty; processed by visual review. |
| `OioUclT-R3w` | 2016-05-07 | Laravel Valet - Installation | 1:57 | none | none | yes, format `251` / opus | ASR unreliable; processed by visual review. |
| `LFY_P-jnuXM` | 2016-01-02 | Laravel Spark Alpha | 1:58 | none | none | yes, format `251` / opus | ASR unreliable; processed by visual review. |

## Checks Performed

- `yt-dlp --list-subs` reported no subtitles and no automatic captions for all three videos.
- `yt-dlp --list-subs --js-runtimes node` also reported no subtitles and no automatic captions for all three videos.
- `yt_dlp` metadata extraction returned empty `subtitles` and `automatic_captions` maps for all three videos.
- Searching by video ID and title did not reveal a public mirrored transcript source.
- `yt-dlp -f ba --print ...` confirmed an audio stream is available for each video.
- `mlx-whisper` with `mlx-community/whisper-base.en-mlx` produced no reliable speech transcript.
- Video-frame visual review produced the source notes in `visual-reviews/`.

## ASR Transcript Convention

ASR transcript attempts are stored under:

```text
data/source/channels/nunomaduro/transcripts/asr/<video-id>.md
```

Each ASR transcript should include:

- Source video URL.
- ASR tool or service name.
- Model name and version when available.
- Generation date.
- A note that the transcript is generated from audio, not provided by YouTube captions.

Do not store downloaded audio or video media in this repository unless that policy is explicitly changed.
