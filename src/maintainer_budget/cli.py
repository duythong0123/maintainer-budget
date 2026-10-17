from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .cluster import cluster_comments
from .exports import render_codex_bundle, render_share_card
from .filtering import filter_actionable
from .github import GitHubClient, GitHubError
from .report import render_markdown, write_json


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-budget",
        description="Find repeated maintainer feedback and turn it into evidence-backed rule candidates.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit", help="Audit recent merged PR review history")
    audit.add_argument("repo", help="GitHub repository in owner/name form")
    audit.add_argument("--max-prs", type=int, default=100, help="Maximum recent merged PRs to inspect")
    audit.add_argument("--min-prs", type=int, default=2, help="Minimum unique PRs required for a candidate")
    audit.add_argument("--similarity", type=float, default=0.34, help="Cosine similarity threshold (0-1)")
    audit.add_argument("--include-issue-comments", action="store_true", help="Also inspect top-level PR conversation comments")
    audit.add_argument("--json", dest="json_path", help="Write machine-readable report to this path")
    audit.add_argument("--output", help="Write Markdown report to this path instead of stdout")
    audit.add_argument("--share-card", help="Write a compact shareable Markdown summary")
    audit.add_argument("--codex-bundle", help="Write an evidence bundle for optional Codex semantic review")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "audit":
        return 2
    if "/" not in args.repo or args.repo.startswith("/") or args.repo.endswith("/"):
        print("error: repo must be in owner/name form", file=sys.stderr)
        return 2
    if not (0.0 < args.similarity <= 1.0):
        print("error: --similarity must be between 0 and 1", file=sys.stderr)
        return 2

    client = GitHubClient()
    try:
        comments = client.collect(
            args.repo,
            max_prs=max(1, args.max_prs),
            include_issue_comments=args.include_issue_comments,
        )
    except GitHubError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    actionable = filter_actionable(comments)
    candidates = cluster_comments(
        actionable,
        similarity_threshold=args.similarity,
        min_unique_prs=max(2, args.min_prs),
    )
    markdown = render_markdown(args.repo, comments, actionable, candidates)

    if args.output:
        Path(args.output).write_text(markdown + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(markdown)

    if args.json_path:
        write_json(args.json_path, args.repo, comments, actionable, candidates)
        print(f"wrote {args.json_path}", file=sys.stderr)

    if args.share_card:
        share = render_share_card(args.repo, comments, actionable, candidates)
        Path(args.share_card).write_text(share + "\n", encoding="utf-8")
        print(f"wrote {args.share_card}", file=sys.stderr)

    if args.codex_bundle:
        bundle = render_codex_bundle(args.repo, candidates)
        Path(args.codex_bundle).write_text(bundle + "\n", encoding="utf-8")
        print(f"wrote {args.codex_bundle}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
