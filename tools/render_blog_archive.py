from __future__ import annotations

import argparse
from pathlib import Path

from tools.blog_archive import write_stitcher_archive
from tools.topic_guides import write_topic_guides


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render blog-source programming guidance.")
    parser.add_argument("--source", choices=["stitcher-io"], required=True, help="Blog source to render.")
    parser.add_argument("--rss", type=Path, required=True, help="RSS XML snapshot for the source.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Repository root to write archive files into.")
    args = parser.parse_args(argv)

    if args.source == "stitcher-io":
        write_stitcher_archive(args.repo, args.rss)

    write_topic_guides(args.repo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
