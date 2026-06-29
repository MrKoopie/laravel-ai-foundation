import unittest

from tools.archive_tools import (
    classify_video,
    extract_helpful_tip_sentences,
    render_video_note,
    slugify_title,
)


class ArchiveToolsTest(unittest.TestCase):
    def test_classifies_obvious_non_programming_videos_as_skipped(self):
        video = {"title": "LoL INSANE VAYNE PLAY | League of Legends", "duration": 28}

        result = classify_video(video)

        self.assertEqual(result["status"], "skipped")
        self.assertIn("not programming", result["reason"])

    def test_classifies_programming_videos_for_processing(self):
        video = {"title": "The Action Pattern Is Key to Clean Code", "duration": 580}

        result = classify_video(video)

        self.assertEqual(result["status"], "needs-processing")
        self.assertIn("clean-code", result["topics"])

    def test_ai_topic_does_not_match_inside_words(self):
        video = {"title": "Advanced PHP: Generics Explained", "duration": 375}

        result = classify_video(video)

        self.assertEqual(result["status"], "needs-processing")
        self.assertIn("php", result["topics"])
        self.assertNotIn("ai", result["topics"])

    def test_slugifies_title_with_video_id_for_stable_filenames(self):
        slug = slugify_title("PHP 8.5: Full Review - What's New & What Changed!", "M1ksgzGbS60")

        self.assertEqual(slug, "php-8-5-full-review-whats-new-what-changed-M1ksgzGbS60")

    def test_extracts_helpful_tip_sentences_from_transcript(self):
        transcript = (
            "You should move validation into a form request. "
            "This keeps controllers small. "
            "What exactly means using this pattern? "
            "I bought a keyboard yesterday. "
            "Back in the days, people used to use a command bus pattern. "
            "Avoid putting business logic directly in controllers."
        )

        tips = extract_helpful_tip_sentences(transcript, limit=3)

        self.assertEqual(
            tips,
            [
                "Move validation into a form request.",
                "Avoid putting business logic directly in controllers.",
            ],
        )

    def test_canonicalizes_known_action_pattern_tips(self):
        transcript = (
            "Super important when you are calling the action you never send any HTTP concern on it. "
            "So you always make sure you call validated to only get validated information. "
            "And also don't worry if the information is not valid. "
            "And why a DB transaction is important when talking about the action pattern. "
            "You don't have to do this kind of request thing. "
            "If any of these pieces fail, you just roll back the entire thing. "
            "Every single time you are performing multiple database actions, you want to roll back the entire process."
        )

        tips = extract_helpful_tip_sentences(transcript, limit=5)

        self.assertEqual(
            tips,
            [
                "Never send HTTP concerns into an action; pass plain validated data instead.",
                "Call `validated()` so actions receive only validated input.",
                "Wrap multi-step mutations in a transaction so partial updates roll back together.",
            ],
        )

    def test_render_skips_sponsor_description_as_programming_summary(self):
        video = {
            "id": "FfDu-XR-8YQ",
            "title": "Laravel Clean Code: How to Write Perfect Form Requests!",
            "upload_date": "20250320",
            "duration_string": "9:40",
            "description": "sponsor this channel: https://example.com\nUse actions to isolate application behavior.",
        }

        rendered = render_video_note(video, "")

        self.assertIn("Use actions to isolate application behavior.", rendered.markdown)
        self.assertNotIn("sponsor this channel", rendered.markdown)

    def test_render_uses_manual_seed_video_notes(self):
        video = {
            "id": "k_gMfdpSXQE",
            "title": "The Action Pattern Is Key to Clean Code",
            "upload_date": "20260603",
            "duration_string": "9:40",
            "description": "",
        }

        rendered = render_video_note(video, "Why a DB transaction is important when talking about the action pattern.")

        self.assertIn("Status: manual-processed", rendered.markdown)
        self.assertIn("Move application behavior into action classes", rendered.markdown)
        self.assertNotIn("Why a DB transaction is important", rendered.markdown)

    def test_render_uses_manual_strict_ai_engineering_notes(self):
        video = {
            "id": "96To5-uJbog",
            "title": "AI Vibe Coding Is Broken. Strict Engineering Fixes It.",
            "upload_date": "20260527",
            "duration_string": "18:39",
            "description": "",
        }

        rendered = render_video_note(video, "For those of you who don't know what is PHP stand.")

        self.assertIn("Status: manual-processed", rendered.markdown)
        self.assertIn("Use PHPStan for PHP and TypeScript for frontend code", rendered.markdown)
        self.assertIn("Treat every generated line as your responsibility", rendered.markdown)
        self.assertNotIn("PHP stand", rendered.markdown)


if __name__ == "__main__":
    unittest.main()
