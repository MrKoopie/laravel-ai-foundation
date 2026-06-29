import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.blog_archive import (
    enrich_stitcher_articles,
    load_stitcher_rss,
    render_curated_article_note,
    write_stitcher_archive,
)
from tools.blog_archive import STITCHER_CURATED_ARTICLES
from tools.render_blog_archive import main as render_blog_archive_main


SAMPLE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <entry>
        <title><![CDATA[Tests and types]]></title>
        <link rel="alternate" href="https://stitcher.io/blog/tests-and-types" />
        <id>https://stitcher.io/blog/tests-and-types</id>
        <updated>2019-06-07T00:00:00.000Z</updated>
        <published>2019-06-07T00:00:00.000Z</published>
        <author><name><![CDATA[Brent]]></name></author>
    </entry>
    <entry>
        <title><![CDATA[Timeline Taxi chapter 01]]></title>
        <link rel="alternate" href="https://stitcher.io/blog/timeline-taxi-chapter-01" />
        <id>https://stitcher.io/blog/timeline-taxi-chapter-01</id>
        <updated>2024-01-01T00:00:00.000Z</updated>
        <published>2024-01-01T00:00:00.000Z</published>
        <author><name><![CDATA[Brent]]></name></author>
    </entry>
</feed>
"""


class BlogArchiveTest(unittest.TestCase):
    def test_loads_stitcher_rss_entries(self):
        with TemporaryDirectory() as tmp:
            rss = Path(tmp) / "rss.xml"
            rss.write_text(SAMPLE_RSS)

            entries = load_stitcher_rss(rss)

        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["slug"], "tests-and-types")
        self.assertEqual(entries[0]["published"], "2019-06-07")
        self.assertEqual(entries[0]["author"], "Brent")

    def test_enriches_curated_and_skipped_articles(self):
        entries = [
            {
                "slug": "tests-and-types",
                "title": "Tests and types",
                "url": "https://stitcher.io/blog/tests-and-types",
                "published": "2019-06-07",
                "author": "Brent",
            },
            {
                "slug": "timeline-taxi-chapter-01",
                "title": "Timeline Taxi chapter 01",
                "url": "https://stitcher.io/blog/timeline-taxi-chapter-01",
                "published": "2024-01-01",
                "author": "Brent",
            },
        ]

        enriched = enrich_stitcher_articles(entries)

        self.assertEqual(enriched[0]["archive_status"], "curated-processed")
        self.assertIn("docs/articles/stitcher-io/2019-06-07-tests-and-types.md", enriched[0]["note_path"])
        self.assertEqual(enriched[1]["archive_status"], "skipped")

    def test_curated_note_keeps_source_and_no_full_copy_marker(self):
        article = next(article for article in STITCHER_CURATED_ARTICLES if article.slug == "tests-and-types")

        markdown = render_curated_article_note(
            article,
            {
                "published": "2019-06-07",
                "author": "Brent",
            },
        )

        self.assertIn("# Tests and types", markdown)
        self.assertIn("URL: https://stitcher.io/blog/tests-and-types", markdown)
        self.assertIn("Guidance is paraphrased", markdown)
        self.assertIn("Constrained value object", markdown)

    def test_renderer_writes_source_inventory_and_notes(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            rss = root / "rss.xml"
            rss.write_text(SAMPLE_RSS)

            exit_code = render_blog_archive_main(
                [
                    "--source",
                    "stitcher-io",
                    "--rss",
                    str(rss),
                    "--repo",
                    str(root),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((root / "data/source/blogs/stitcher-io/source.json").exists())
            self.assertTrue((root / "data/source/blogs/stitcher-io/rss.raw.xml").exists())
            self.assertTrue((root / "docs/articles/stitcher-io/2019-06-07-tests-and-types.md").exists())
            self.assertTrue((root / "docs/indexes/blog-sources.md").exists())

            articles = [
                json.loads(line)
                for line in (root / "data/source/blogs/stitcher-io/articles.jsonl").read_text().splitlines()
                if line.strip()
            ]
            self.assertEqual(articles[0]["archive_status"], "curated-processed")

    def test_write_stitcher_archive_returns_enriched_articles(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            rss = root / "rss.xml"
            rss.write_text(SAMPLE_RSS)

            articles = write_stitcher_archive(root, rss)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]["archive_status"], "curated-processed")


if __name__ == "__main__":
    unittest.main()
