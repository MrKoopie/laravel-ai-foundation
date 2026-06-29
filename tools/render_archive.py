from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from tools.archive_tools import (
    classify_video,
    render_topic_index,
    render_video_note,
    render_videos_index,
    write_text,
)
from tools.topic_guides import write_topic_guides


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render the nunomaduro programming tips archive.")
    parser.add_argument("--metadata", type=Path, required=True, help="JSONL file from yt-dlp compact metadata output.")
    parser.add_argument("--captions", type=Path, default=None, help="Optional directory containing caption files named <video-id>.*.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Repository root to write archive files into.")
    parser.add_argument("--channel-slug", default="nunomaduro", help="Source channel slug for generated metadata.")
    args = parser.parse_args(argv)

    videos = load_jsonl(args.metadata)
    notes = []

    for video in videos:
        classification = classify_video(video)
        if classification["status"] != "needs-processing":
            continue

        transcript = load_caption_text(args.captions, str(video["id"])) if args.captions else ""
        rendered = render_video_note(video, transcript)
        note_path = Path("docs/videos") / rendered.filename
        write_text(args.repo / note_path, rendered.markdown)

        video["archive_status"] = rendered.status
        video["note_path"] = str(note_path)
        notes.append(
            {
                "title": video["title"],
                "filename": rendered.filename,
                "topics": classification["topics"],
            }
        )

    write_text(args.repo / "videos.md", render_videos_index(videos))
    write_text(args.repo / "docs/indexes/video-topics.md", render_topic_index(notes))
    write_topic_guides(args.repo)
    source_path = args.repo / "data/source/channels" / args.channel_slug / "videos.jsonl"
    write_text(source_path, "\n".join(json.dumps(video, ensure_ascii=False) for video in videos) + "\n")

    return 0


def load_jsonl(path: Path) -> list[dict]:
    videos = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            videos.append(json.loads(line))
    return videos


def load_caption_text(captions_dir: Path | None, video_id: str) -> str:
    if captions_dir is None or not captions_dir.exists():
        return ""

    candidates = sorted(captions_dir.glob(f"{video_id}.*"))
    for candidate in candidates:
        if candidate.suffix == ".json3":
            return parse_json3_caption(candidate)
        if candidate.suffix in {".vtt", ".srt"}:
            return parse_text_caption(candidate)

    return ""


def parse_json3_caption(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    parts = []
    for event in payload.get("events", []):
        for segment in event.get("segs", []) or []:
            text = segment.get("utf8", "").strip()
            if text:
                parts.append(text)
    return normalize_caption_text(" ".join(parts))


def parse_text_caption(path: Path) -> str:
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.isdigit() or "-->" in line or line.upper().startswith("WEBVTT"):
            continue
        lines.append(line)
    return normalize_caption_text(" ".join(lines))


def normalize_caption_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


if __name__ == "__main__":
    raise SystemExit(main())
