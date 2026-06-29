import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOST_AGENT_KEYS = [
    "amp",
    "junie",
    "cursor",
    "claude_code",
    "codex",
    "copilot",
    "factory",
    "kiro",
    "opencode",
    "antigravity",
    "zed",
    "pi",
]


class RepositoryMetadataTest(unittest.TestCase):
    def test_boost_configuration_is_present_and_docs_repo_scoped(self):
        config = json.loads((ROOT / "boost.json").read_text())

        self.assertEqual(config["agents"], BOOST_AGENT_KEYS)
        self.assertTrue(config["guidelines"])
        self.assertFalse(config["mcp"])
        self.assertFalse(config["sail"])
        self.assertFalse(config["nightwatch"])
        self.assertFalse(config["cloud"])
        self.assertEqual(config["packages"], [])
        self.assertEqual(config["skills"], [])

    def test_boost_guidance_files_exist(self):
        agents = (ROOT / "AGENTS.md").read_text()
        claude = (ROOT / "CLAUDE.md").read_text()
        guideline = (ROOT / ".ai/guidelines/programming-foundation.md").read_text()

        self.assertIn("Generated Documentation Workflow", agents)
        self.assertIn("Boost Compatibility", agents)
        self.assertIn("AGENTS.md", claude)
        self.assertIn("claude_code", claude)
        self.assertIn("Search Surface", guideline)
        self.assertIn("Content Rules", guideline)

    def test_coderabbit_is_disabled_for_this_repo(self):
        config = (ROOT / ".coderabbit.yaml").read_text()

        self.assertIn("CodeRabbit is intentionally disabled", config)
        self.assertIn("reviews:", config)
        self.assertIn("auto_review:", config)
        self.assertIn("enabled: false", config)
        self.assertIn("auto_reply: false", config)
        self.assertIn("issue_enrichment:", config)

    def test_source_artifacts_are_checked_in_for_reanalysis(self):
        source_dir = ROOT / "data/source/channels/nunomaduro"
        captions_dir = source_dir / "captions/youtube-json3"

        self.assertTrue((source_dir / "youtube-videos.raw.jsonl").exists())
        self.assertTrue((source_dir / "videos.jsonl").exists())
        self.assertTrue((source_dir / "programming-video-urls.txt").exists())
        self.assertTrue((source_dir / "README.md").exists())
        self.assertTrue((source_dir / "channel.json").exists())
        self.assertTrue((source_dir / "transcript-audit.md").exists())
        self.assertTrue((source_dir / "transcript-source-methods.md").exists())
        self.assertTrue((source_dir / "transcripts/README.md").exists())
        self.assertGreaterEqual(len(list(captions_dir.glob("*.json3"))), 180)

    def test_blog_source_artifacts_are_checked_in_for_reanalysis(self):
        source_dir = ROOT / "data/source/blogs/stitcher-io"
        source_config = json.loads((source_dir / "source.json").read_text())
        articles = [
            json.loads(line)
            for line in (source_dir / "articles.jsonl").read_text().splitlines()
            if line.strip()
        ]

        self.assertTrue((ROOT / "data/source/blogs/README.md").exists())
        self.assertTrue((source_dir / "README.md").exists())
        self.assertTrue((source_dir / "rss.raw.xml").exists())
        self.assertTrue((source_dir / "articles.raw.jsonl").exists())
        self.assertTrue((source_dir / "articles.md").exists())
        self.assertEqual(source_config["slug"], "stitcher-io")
        self.assertEqual(source_config["rss"], "https://stitcher.io/rss")
        self.assertGreaterEqual(len(articles), 250)
        self.assertGreaterEqual(
            sum(1 for article in articles if article["archive_status"] == "curated-processed"),
            20,
        )
        self.assertTrue((ROOT / "docs/articles/stitcher-io/2019-06-07-tests-and-types.md").exists())
        self.assertTrue((ROOT / "docs/indexes/blog-sources.md").exists())

    def test_source_layout_is_grouped_by_channel(self):
        source_dir = ROOT / "data/source"
        channel_config = json.loads((source_dir / "channels/nunomaduro/channel.json").read_text())

        self.assertTrue((source_dir / "channels/README.md").exists())
        self.assertEqual(channel_config["slug"], "nunomaduro")
        self.assertEqual(channel_config["handle"], "@nunomaduro")
        self.assertEqual(channel_config["artifacts"]["captions"], "captions/youtube-json3")
        self.assertEqual(channel_config["artifacts"]["transcriptAudit"], "transcript-audit.md")
        self.assertEqual(channel_config["artifacts"]["transcriptSourceMethods"], "transcript-source-methods.md")
        self.assertEqual(channel_config["artifacts"]["asrTranscripts"], "transcripts/asr")
        self.assertEqual(channel_config["artifacts"]["visualReviews"], "visual-reviews")
        self.assertFalse((source_dir / "videos.jsonl").exists())
        self.assertFalse((source_dir / "youtube-videos.raw.jsonl").exists())
        self.assertFalse((source_dir / "programming-video-urls.txt").exists())

    def test_source_layout_is_grouped_by_blog(self):
        source_dir = ROOT / "data/source"
        blog_config = json.loads((source_dir / "blogs/stitcher-io/source.json").read_text())

        self.assertTrue((source_dir / "blogs/README.md").exists())
        self.assertEqual(blog_config["slug"], "stitcher-io")
        self.assertEqual(blog_config["url"], "https://stitcher.io/")
        self.assertFalse((source_dir / "articles.jsonl").exists())
        self.assertFalse((source_dir / "rss.raw.xml").exists())

    def test_missing_transcript_audit_lists_all_current_gaps(self):
        audit = (ROOT / "data/source/channels/nunomaduro/transcript-audit.md").read_text()

        self.assertIn("UQ6JrEsyvvw", audit)
        self.assertIn("OioUclT-R3w", audit)
        self.assertIn("LFY_P-jnuXM", audit)
        self.assertIn("none | none", audit)
        self.assertIn("processed by visual review", audit)

    def test_visual_review_and_asr_attempts_are_stored_for_silent_videos(self):
        source_dir = ROOT / "data/source/channels/nunomaduro"

        for video_id in ["UQ6JrEsyvvw", "OioUclT-R3w", "LFY_P-jnuXM"]:
            self.assertTrue((source_dir / f"visual-reviews/{video_id}.md").exists())
            self.assertTrue((source_dir / f"transcripts/asr/{video_id}.md").exists())

    def test_transcript_source_methods_document_alternative_routes(self):
        methods = (ROOT / "data/source/channels/nunomaduro/transcript-source-methods.md").read_text()

        self.assertIn("GMUkj23bznA", methods)
        self.assertIn("yt-dlp Automatic Captions", methods)
        self.assertIn("YouTube Timedtext Endpoint", methods)
        self.assertIn("Third-Party Transcript Pages", methods)
        self.assertIn("not as a separate source of truth", methods)

    def test_context7_keeps_search_focused_on_docs(self):
        config = json.loads((ROOT / "context7.json").read_text())

        self.assertEqual(config["folders"], ["docs"])
        self.assertIn("tools", config["excludeFolders"])
        self.assertIn("data", config["excludeFolders"])
        self.assertIn("README.md", config["excludeFiles"])
        self.assertIn("AGENTS.md", config["excludeFiles"])
        self.assertIn("CLAUDE.md", config["excludeFiles"])
        self.assertIn("videos.md", config["excludeFiles"])

    def test_codex_plugin_exposes_foundation_skill(self):
        plugin = json.loads(
            (ROOT / "plugins/laravel-ai-foundation/.codex-plugin/plugin.json").read_text()
        )
        skill = (
            ROOT
            / "plugins/laravel-ai-foundation/skills/laravel-ai-foundation/SKILL.md"
        ).read_text()
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())

        self.assertEqual(plugin["name"], "laravel-ai-foundation")
        self.assertEqual(plugin["skills"], "./skills/")
        self.assertIn("Context7", skill)
        self.assertIn("/mrkoopie/laravel-ai-foundation", skill)
        self.assertIn("actions are not the default", skill)
        self.assertIn("official Laravel documentation", skill)
        self.assertEqual(marketplace["name"], "programming-foundation")
        self.assertEqual(marketplace["plugins"][0]["name"], "laravel-ai-foundation")


if __name__ == "__main__":
    unittest.main()
