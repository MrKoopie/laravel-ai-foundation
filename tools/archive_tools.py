from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


PROGRAMMING_TOPIC_KEYWORDS = {
    "ai": ["ai", "agent", "claude", "cursor", "devin", "junie", "opus", "vibe coding"],
    "architecture": ["action pattern", "design pattern", "dto", "event sourcing", "factory", "builder"],
    "clean-code": ["clean code", "strict equality", "controller", "form request", "appserviceprovider"],
    "database": ["database", "db", "migration", "transaction", "unique constraint", "cascade"],
    "frontend": ["react", "vue", "svelte", "next.js", "tanstack", "inertia", "livewire"],
    "laravel": ["laravel", "artisan", "blade", "filament", "flux", "pail", "pint", "reverb", "valet", "vapor"],
    "open-source": ["contribute", "open source", "packagist", "package"],
    "php": ["php", "composer", "frankenphp", "generics", "larastan", "mago", "peck", "phpstan", "rector"],
    "productivity": ["productivity", "setup", "terminal", "tools", "workflow"],
    "rust": ["rust"],
    "security": ["security", "supply chain"],
    "testing": ["test", "testing", "pest", "phpunit", "snapshot", "smoke", "mock"],
    "tooling": ["editorconfig", "gitattributes", "gitignore", "mcp", "playwright", "typesense", "ziggy"],
}

NON_PROGRAMMING_KEYWORDS = [
    "league of legends",
    "lol ",
    "jazz",
    "music anthem",
    "motivational speech",
    "day in the life",
    "say hi to light mode",
    "tomorrow.",
]

LOW_VALUE_PROGRAMMING_ADJACENT = [
    "will ai replace programmers",
    "truth behind tech ai layoffs",
    "laravel's president explains",
    "my 2024:",
    "who is the pest team",
]

TIP_CUES = [
    "always",
    "avoid",
    "don't",
    "do not",
    "instead",
    "make sure",
    "need to",
    "never",
    "prefer",
    "recommend",
    "should",
    "stop",
    "use ",
]

MANUAL_VIDEO_NOTES = {
    "k_gMfdpSXQE": {
        "summary": "Explains the Laravel action pattern as a way to keep controllers thin, isolate application behavior, and make business workflows reusable outside HTTP requests.",
        "tips": [
            "Move application behavior into action classes instead of packing it into controllers.",
            "Keep HTTP concerns out of actions; pass plain validated data rather than request objects.",
            "Use form requests at the boundary, then call `validated()` before handing data to an action.",
            "Wrap multi-step mutations in a transaction so partial updates roll back together.",
            "Reuse actions from controllers, jobs, commands, or other actions when the same behavior is needed in multiple entry points.",
            "Use arrays or DTOs deliberately for action input; choose the structure that makes the boundary clear without overcomplicating the call site.",
        ],
    },
    "96To5-uJbog": {
        "summary": "Argues that AI-assisted coding only works well when the project already has strict engineering guardrails. Treat every generated line as your responsibility, and use strong typing, conventions, static analysis, linting, tests, coverage, CI, and explicit AI instructions to push generated code toward production quality.",
        "tips": [
            "00:21 - Make types the first AI guardrail. Use PHPStan for PHP and TypeScript for frontend code so generated mistakes are caught across the whole project.",
            "01:02 - Run static analysis against real application mistakes. Tools should verify generated code against model properties, imports, and symbols, not just against the file currently open in the editor.",
            "02:11 - Apply the same strictness to frontend code. TypeScript should catch bad imports and missing components before AI-generated React or Inertia code reaches review.",
            "03:24 - Keep conventions consistent because AI agents copy what they inspect. Typed classes, form requests, actions, clean migrations, and predictable structure give the agent better examples to imitate.",
            "04:20 - Use strict PHP defaults everywhere. Strict types and native type declarations give humans, tools, and AI a clearer contract than loose code plus vague comments.",
            "05:11 - Standardize Laravel boundaries. Keep validation in form requests, orchestration in controllers or actions, and business behavior in dedicated classes so generated code has obvious places to go.",
            "06:23 - Treat the quality pipeline as more than unit tests. Formatting, linting, type coverage, code coverage, static analysis, and tests are the safety net for AI-assisted changes.",
            "07:15 - Hide quality tooling behind Composer scripts. Commands like `composer lint` and `composer test` give teammates, CI, and AI agents stable entry points for the same checks.",
            "08:18 - Separate local fixing from CI checking. Let local lint commands format or fix code, but make CI verify formatting without mutating files.",
            "08:48 - Enforce type coverage. Failing the build for missing types turns typed code from a preference into an automated rule.",
            "10:14 - Run tests in parallel and require coverage so strict checks stay practical and AI-generated features include tests, not only implementation.",
            "11:54 - Add AI-specific project instructions that tell agents to run the full test command before finishing and to follow the repository's established conventions.",
        ],
    },
    "UQ6JrEsyvvw": {
        "summary": "Silent visual demo of installing a small Laravel package and smoke-testing that its Artisan command is discovered and executable.",
        "tips": [
            "Use the smallest observable CLI behavior when testing a package install; here the command signature is `plus` and `handle()` prints a success message.",
            "Install a local or development Composer package into a real Laravel app to verify autoloading and package discovery outside the package repository.",
            "After Composer updates autoload files, run the package-provided Artisan command immediately as a smoke test.",
            "A command that prints an explicit success message makes the package registration test obvious and fast to repeat.",
        ],
        "source_notes": [
            "No YouTube transcript or automatic captions were available.",
            "ASR produced no reliable speech transcript.",
            "Tips are based on visual review notes in data/source/channels/nunomaduro/visual-reviews/UQ6JrEsyvvw.md.",
        ],
    },
    "OioUclT-R3w": {
        "summary": "Silent visual walkthrough of installing Laravel Valet on macOS by checking prerequisites, installing the global CLI, running the installer, and verifying a local domain.",
        "tips": [
            "Treat local-development tooling setup as a checklist: update Homebrew, confirm service management is available, install the required PHP runtime, and only then install the tool.",
            "When installing a global Composer CLI, make sure Composer's global bin directory is on `PATH` before expecting shell commands to work.",
            "Run the tool's installer command after the package install; for Valet this is the step that configures the system services.",
            "Verify the installation with a real project directory and a browser request to the local development domain instead of stopping after the install command succeeds.",
        ],
        "source_notes": [
            "No YouTube transcript or automatic captions were available.",
            "ASR produced no reliable speech transcript.",
            "Tips are based on visual review notes in data/source/channels/nunomaduro/visual-reviews/OioUclT-R3w.md.",
        ],
    },
    "LFY_P-jnuXM": {
        "summary": "Silent visual tour of Laravel Spark alpha showing SaaS scaffolding screens such as onboarding, settings, security, subscription, invoices, and teams.",
        "tips": [
            "Evaluate starter kits by walking through the full product flow, not only by checking that the app boots.",
            "Use generated SaaS scaffolding as an acceptance checklist: registration, profile settings, password changes, two-factor setup, subscriptions, invoices, and teams should all be exercised.",
            "Inspect the configuration or code behind plan and team setup before extending billing behavior.",
            "Treat historical alpha-product walkthroughs as pattern references, not as code to copy directly into a modern app.",
        ],
        "source_notes": [
            "No YouTube transcript or automatic captions were available.",
            "ASR produced no reliable speech transcript.",
            "Tips are based on visual review notes in data/source/channels/nunomaduro/visual-reviews/LFY_P-jnuXM.md.",
        ],
    },
}


@dataclass(frozen=True)
class RenderedVideo:
    filename: str
    markdown: str
    status: str


def classify_video(video: dict) -> dict:
    title = str(video.get("title") or "")
    title_lower = title.lower()

    if any(keyword in title_lower for keyword in NON_PROGRAMMING_KEYWORDS):
        return {
            "status": "skipped",
            "reason": "not programming-useful content",
            "topics": [],
        }

    if any(keyword in title_lower for keyword in LOW_VALUE_PROGRAMMING_ADJACENT):
        return {
            "status": "skipped",
            "reason": "programming-adjacent but not a reusable programming tip source",
            "topics": [],
        }

    topics = [
        topic
        for topic, keywords in PROGRAMMING_TOPIC_KEYWORDS.items()
        if any(_title_contains(title_lower, keyword) for keyword in keywords)
    ]

    if topics:
        return {
            "status": "needs-processing",
            "reason": "programming-useful topic",
            "topics": sorted(topics),
        }

    return {
        "status": "skipped",
        "reason": "no clear reusable programming tips detected from metadata",
        "topics": [],
    }


def slugify_title(title: str, video_id: str) -> str:
    ascii_title = (
        title.encode("ascii", "ignore")
        .decode("ascii")
    )
    ascii_title = re.sub(r"['’]", "", ascii_title)
    ascii_title = ascii_title.replace("&", " ").replace("+", " plus ")
    slug = re.sub(r"[^A-Za-z0-9]+", "-", ascii_title).strip("-").lower()
    slug = re.sub(r"-{2,}", "-", slug)
    return f"{slug[:72].strip('-')}-{video_id}"


def normalize_upload_date(upload_date: str | None, timestamp: int | None = None) -> str:
    if upload_date and re.fullmatch(r"\d{8}", upload_date):
        return f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    if timestamp:
        return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    return "unknown-date"


def extract_helpful_tip_sentences(transcript: str, limit: int = 8) -> list[str]:
    cleaned = re.sub(r"\s+", " ", transcript).strip()
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    tips: list[str] = []
    seen: set[str] = set()

    for sentence in sentences:
        normalized = _normalize_tip_sentence(sentence)
        if not normalized:
            continue

        canonical = _canonicalize_known_tip(normalized)
        if canonical:
            key = canonical.lower()
            if key not in seen:
                seen.add(key)
                tips.append(canonical)
            if len(tips) >= limit:
                break
            continue

        lowered = normalized.lower()
        if not any(cue in lowered for cue in TIP_CUES):
            continue

        actionable = _make_tip_actionable(normalized)
        key = actionable.lower()
        if key in seen:
            continue

        seen.add(key)
        tips.append(actionable)
        if len(tips) >= limit:
            break

    return tips


def render_video_note(video: dict, transcript: str = "") -> RenderedVideo:
    video_id = str(video.get("id") or "")
    title = str(video.get("title") or video_id)
    upload_date = normalize_upload_date(video.get("upload_date"), video.get("timestamp"))
    classification = classify_video(video)
    topics = classification["topics"]
    manual_note = MANUAL_VIDEO_NOTES.get(video_id)
    status = "manual-processed" if manual_note else ("auto-processed" if transcript else "needs-transcript-review")
    tips = manual_note["tips"] if manual_note else extract_helpful_tip_sentences(transcript)

    filename = f"{upload_date}-{slugify_title(title, video_id)}.md"
    url = f"https://www.youtube.com/watch?v={video_id}"
    duration = video.get("duration_string") or _format_duration(video.get("duration"))
    description = _first_useful_description_line(str(video.get("description") or ""))

    lines = [
        f"# {title}",
        "",
        f"URL: {url}",
        "Channel: [nunomaduro](https://www.youtube.com/@nunomaduro)",
        f"Upload date: {upload_date}",
        f"Duration: {duration}",
        f"Status: {status}",
        f"Topics: {', '.join(topics) if topics else 'uncategorized'}",
        "",
        "## Why This Helps Programming",
        manual_note["summary"] if manual_note else (description or _topic_summary(title, topics)),
        "",
        "## Tips And Tricks",
    ]

    if tips:
        lines.extend(f"- {tip}" for tip in tips)
    else:
        lines.append("- No transcript-derived tips were available. Review the video manually before treating it as processed knowledge.")

    source_notes = (
        manual_note.get("source_notes", [])
        if manual_note and manual_note.get("source_notes")
        else ["Tips are paraphrased or normalized from available YouTube captions/metadata."]
    )

    lines.extend(
        [
            "",
            "## Source Notes",
            *(f"- {source_note}" for source_note in source_notes),
            "- Video media is not stored in this repository.",
            "",
        ]
    )

    return RenderedVideo(filename=filename, markdown="\n".join(lines), status=status)


def render_videos_index(videos: Iterable[dict]) -> str:
    rows = [
        "# Video Processing Tracker",
        "",
        "Source channel: [nunomaduro](https://www.youtube.com/@nunomaduro)",
        "",
        "| Status | Upload Date | Title | URL | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]

    for video in videos:
        classification = classify_video(video)
        upload_date = normalize_upload_date(video.get("upload_date"), video.get("timestamp"))
        title = _escape_table(str(video.get("title") or "Untitled"))
        video_id = str(video.get("id") or "")
        url = f"https://www.youtube.com/watch?v={video_id}"
        status = classification["status"]
        notes = classification["reason"]
        if status == "needs-processing":
            status = str(video.get("archive_status") or status)
            note_path = video.get("note_path")
            if note_path:
                notes = f"[note]({note_path})"

        rows.append(f"| {status} | {upload_date} | {title} | {url} | {notes} |")

    rows.append("")
    return "\n".join(rows)


def render_topic_index(video_notes: Iterable[dict]) -> str:
    topics: dict[str, list[dict]] = {}
    for note in video_notes:
        for topic in note.get("topics", []):
            topics.setdefault(topic, []).append(note)

    lines = [
        "# Topic Index",
        "",
        "Use this page to jump from a programming topic to the related video notes.",
        "",
    ]

    for topic in sorted(topics):
        lines.extend([f"## {topic}", ""])
        for note in sorted(topics[topic], key=lambda item: item["title"].lower()):
            lines.append(f"- [{note['title']}](../videos/{note['filename']})")
        lines.append("")

    return "\n".join(lines)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _normalize_tip_sentence(sentence: str) -> str:
    sentence = re.sub(r"\[[^\]]+\]", "", sentence)
    sentence = re.sub(r"\s+", " ", sentence).strip(" -\t\r\n")
    lowered = sentence.lower()
    if sentence.endswith("?"):
        return ""
    if re.match(r"^(what|when|where|why|how)\b", sentence, flags=re.IGNORECASE):
        return ""
    if lowered.startswith(("back in the days", "don't worry", "dont worry", "and why", "and also don't worry", "and also dont worry")):
        return ""
    if "you don't have to do this kind" in lowered or "you dont have to do this kind" in lowered:
        return ""
    if len(sentence) < 16 or len(sentence) > 240:
        return ""
    if sentence.count(" ") < 3:
        return ""
    return sentence


def _make_tip_actionable(sentence: str) -> str:
    sentence = re.sub(r"^(now|so|and also),?\s+", "", sentence, flags=re.IGNORECASE)
    sentence = re.sub(r"^(you|we|i)\s+should\s+", "", sentence, flags=re.IGNORECASE)
    sentence = re.sub(r"^you\s+need\s+to\s+", "", sentence, flags=re.IGNORECASE)
    sentence = re.sub(r"^you\s+can\s+", "", sentence, flags=re.IGNORECASE)
    sentence = sentence[:1].upper() + sentence[1:]
    if not sentence.endswith((".", "!", "?")):
        sentence += "."
    return sentence


def _canonicalize_known_tip(sentence: str) -> str:
    lowered = sentence.lower()
    if "never send any http concern" in lowered:
        return "Never send HTTP concerns into an action; pass plain validated data instead."
    if "call validated" in lowered and "validated information" in lowered:
        return "Call `validated()` so actions receive only validated input."
    if "roll back the entire thing" in lowered or "roll back the entire process" in lowered or ("pieces fail" in lowered and "roll back" in lowered):
        return "Wrap multi-step mutations in a transaction so partial updates roll back together."
    if "make sure you validate the data" in lowered:
        return "Validate request data before passing it into application actions."
    return ""


def _format_duration(duration: object) -> str:
    if not duration:
        return "unknown"
    seconds = int(float(duration))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def _first_useful_description_line(description: str) -> str:
    for line in description.splitlines():
        line = line.strip()
        if not line:
            continue
        lowered = line.lower()
        if line.startswith(("http://", "https://", "#")):
            continue
        if "http://" in lowered or "https://" in lowered:
            continue
        if any(word in lowered for word in ["sponsor", "subscribe", "newsletter", "discord"]):
            continue
        if len(line) < 12:
            continue
        return line
    return ""


def _topic_summary(title: str, topics: list[str]) -> str:
    if topics:
        return f"This video appears to cover {', '.join(topics)} practices that can be reused in day-to-day programming work."
    return f"This video was selected as programming-useful based on its title: {title}."


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def _title_contains(title_lower: str, keyword: str) -> bool:
    keyword_lower = keyword.lower()
    if re.fullmatch(r"[a-z0-9]{1,3}", keyword_lower):
        return re.search(rf"(?<![a-z0-9]){re.escape(keyword_lower)}(?![a-z0-9])", title_lower) is not None
    return keyword_lower in title_lower
