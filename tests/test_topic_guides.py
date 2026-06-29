import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.render_archive import main as render_archive_main
from tools.topic_guides import (
    TopicGuide,
    render_examples_index,
    render_topic_guide,
    render_topic_landing,
)


class TopicGuidesTest(unittest.TestCase):
    def test_render_topic_guide_has_searchable_structure(self):
        guide = TopicGuide(
            slug="strict-ai-engineering",
            title="Strict AI Engineering",
            description="Use guardrails so AI-generated code stays reviewable.",
            rules=["Run static analysis before accepting generated code."],
            tips=[
                {
                    "title": "Use types as guardrails",
                    "body": "Use PHPStan and TypeScript to catch generated mistakes.",
                    "source": "docs/videos/example.md",
                }
            ],
            examples=[
                {
                    "title": "Composer quality script",
                    "language": "json",
                    "code": '{"scripts": {"test": "pest"}}',
                    "body": "Expose one command that agents and CI can both run.",
                }
            ],
            source_videos=[
                {
                    "title": "AI Vibe Coding Is Broken. Strict Engineering Fixes It.",
                    "path": "docs/videos/example.md",
                }
            ],
            related=["testing"],
            source_articles=[
                {
                    "title": "Tests and types",
                    "path": "docs/articles/stitcher-io/example.md",
                }
            ],
        )

        markdown = render_topic_guide(guide)

        self.assertIn("# Strict AI Engineering", markdown)
        self.assertIn("## Practical Rules", markdown)
        self.assertIn("## Tips And Tricks", markdown)
        self.assertIn("Use PHPStan and TypeScript", markdown)
        self.assertIn("## Examples", markdown)
        self.assertIn("```json", markdown)
        self.assertIn("[AI Vibe Coding Is Broken", markdown)
        self.assertIn("## Source Articles", markdown)
        self.assertIn("[Tests and types](../articles/stitcher-io/example.md)", markdown)

    def test_topic_landing_links_to_guides(self):
        markdown = render_topic_landing(
            [
                TopicGuide(
                    slug="testing",
                    title="Testing",
                    description="Testing practices.",
                    rules=[],
                    tips=[],
                    examples=[],
                    source_videos=[],
                    related=[],
                )
            ]
        )

        self.assertIn("# Topic Guides", markdown)
        self.assertIn("[Testing](../topics/testing.md)", markdown)
        self.assertIn("[Blog source index](blog-sources.md)", markdown)

    def test_new_blog_backed_topic_guides_are_present(self):
        from tools.topic_guides import TOPIC_GUIDES

        slugs = {guide.slug for guide in TOPIC_GUIDES}

        self.assertIn("request-data-boundaries", slugs)
        self.assertIn("domain-modeling", slugs)
        self.assertIn("event-sourcing", slugs)
        self.assertIn("dependencies-and-maintenance", slugs)

    def test_examples_index_links_to_topic_examples(self):
        guide = TopicGuide(
            slug="laravel-actions",
            title="Laravel Actions",
            description="Action pattern.",
            rules=[],
            tips=[],
            examples=[
                {
                    "title": "Action class",
                    "language": "php",
                    "code": "<?php\nfinal class CreateUser {}\n",
                    "body": "Keep behavior reusable.",
                }
            ],
            source_videos=[],
            related=[],
        )

        markdown = render_examples_index([guide])

        self.assertIn("# Examples", markdown)
        self.assertIn("## Laravel Actions", markdown)
        self.assertIn("```php", markdown)
        self.assertIn("final class CreateUser", markdown)

    def test_laravel_actions_explains_why_validation_stays_outside_action(self):
        from tools.topic_guides import TOPIC_GUIDES

        guide = next(guide for guide in TOPIC_GUIDES if guide.slug == "laravel-actions")

        markdown = render_topic_guide(guide)

        self.assertIn("validation is a boundary concern", markdown)
        self.assertIn("HTTP requests, queued jobs, console commands, and tests", markdown)
        self.assertIn("trusted, already-shaped input", markdown)

    def test_archive_renderer_writes_topic_guides(self):
        metadata = (
            '{"id":"96To5-uJbog","title":"AI Vibe Coding Is Broken. Strict Engineering Fixes It.",'
            '"upload_date":"20260527","duration":1119,"duration_string":"18:39",'
            '"webpage_url":"https://www.youtube.com/watch?v=96To5-uJbog","description":""}\n'
        )

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata_path = root / "videos.jsonl"
            metadata_path.write_text(metadata)

            exit_code = render_archive_main(
                [
                    "--metadata",
                    str(metadata_path),
                    "--repo",
                    str(root),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((root / "docs/topics/ai-engineering.md").exists())
            self.assertTrue((root / "docs/examples/index.md").exists())
            self.assertTrue((root / "docs/indexes/video-topics.md").exists())
            self.assertTrue((root / "data/source/channels/nunomaduro/videos.jsonl").exists())

    def test_archive_renderer_writes_enriched_metadata_to_requested_channel(self):
        metadata = (
            '{"id":"96To5-uJbog","title":"AI Vibe Coding Is Broken. Strict Engineering Fixes It.",'
            '"upload_date":"20260527","duration":1119,"duration_string":"18:39",'
            '"webpage_url":"https://www.youtube.com/watch?v=96To5-uJbog","description":""}\n'
        )

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata_path = root / "videos.jsonl"
            metadata_path.write_text(metadata)

            exit_code = render_archive_main(
                [
                    "--metadata",
                    str(metadata_path),
                    "--channel-slug",
                    "example-channel",
                    "--repo",
                    str(root),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((root / "data/source/channels/example-channel/videos.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
