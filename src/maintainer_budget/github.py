from __future__ import annotations

import json
import os
import time
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .models import ReviewComment

API_ROOT = "https://api.github.com"


class GitHubError(RuntimeError):
    pass


def _number_from_api_url(url: str | None) -> int | None:
    if not url:
        return None
    try:
        return int(url.rstrip("/").rsplit("/", 1)[-1])
    except (TypeError, ValueError):
        return None


class GitHubClient:
    def __init__(self, token: str | None = None, *, timeout: int = 30):
        self.token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        self.timeout = timeout

    def _get(self, path: str, params: dict[str, object] | None = None):
        url = f"{API_ROOT}{path}"
        if params:
            url += "?" + urlencode(params)
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "maintainer-budget/0.1",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(url, headers=headers)
        for attempt in range(3):
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    return json.load(response)
            except HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                # GitHub sometimes returns transient gateway errors for public
                # repositories. Do not retry permission failures or quota 403.
                if exc.code in (429, 502, 503, 504) and attempt < 2:
                    time.sleep(1 << attempt)
                    continue
                raise GitHubError(f"GitHub API {exc.code}: {body[:500]}") from exc
            except URLError as exc:
                if attempt < 2:
                    time.sleep(1 << attempt)
                    continue
                raise GitHubError(f"GitHub API connection failed: {exc.reason}") from exc

    def _paged(self, path: str, *, max_pages: int = 100, extra: dict[str, object] | None = None):
        items = []
        for page in range(1, max_pages + 1):
            params = {"per_page": 100, "page": page}
            if extra:
                params.update(extra)
            batch = self._get(path, params)
            if not isinstance(batch, list):
                raise GitHubError(f"Expected list from {path}")
            items.extend(batch)
            if len(batch) < 100:
                break
            if page == max_pages:
                raise GitHubError(
                    f"Review history exceeded the {max_pages}-page safety limit for {path}; "
                    "refusing to return a silently incomplete audit."
                )
            time.sleep(0.05)
        return items

    def merged_pull_requests(self, repo: str, *, max_prs: int = 100) -> list[dict]:
        pulls: list[dict] = []
        page = 1
        while len(pulls) < max_prs:
            batch = self._get(
                f"/repos/{repo}/pulls",
                {
                    "state": "closed",
                    "sort": "updated",
                    "direction": "desc",
                    "per_page": 100,
                    "page": page,
                },
            )
            if not batch:
                break
            pulls.extend(p for p in batch if p.get("merged_at"))
            if len(batch) < 100:
                break
            page += 1
        return pulls[:max_prs]

    def repository_review_comments(
        self,
        repo: str,
        *,
        pr_numbers: set[int],
        since: str | None = None,
    ) -> list[ReviewComment]:
        """Collect review comments for target PRs with repository-level pagination.

        GitHub exposes all pull-request review comments for a repository in one
        paginated endpoint. Fetching that window once avoids the previous N+1
        pattern of one HTTP request per pull request.
        """
        if not pr_numbers:
            return []
        extra: dict[str, object] = {"sort": "created", "direction": "asc"}
        if since:
            extra["since"] = since
        raw = self._paged(f"/repos/{repo}/pulls/comments", extra=extra)
        comments: list[ReviewComment] = []
        for item in raw:
            pr_number = _number_from_api_url(item.get("pull_request_url"))
            if pr_number not in pr_numbers:
                continue
            user = item.get("user") or {}
            comments.append(
                ReviewComment(
                    repo=repo,
                    pr_number=pr_number,
                    url=item.get("html_url") or item.get("url") or "",
                    author=user.get("login") or "unknown",
                    author_type=user.get("type"),
                    body=item.get("body") or "",
                    path=item.get("path"),
                    created_at=item.get("created_at"),
                    author_association=item.get("author_association"),
                )
            )
        return comments

    def repository_issue_comments(
        self,
        repo: str,
        *,
        pr_numbers: set[int],
        since: str | None = None,
    ) -> list[ReviewComment]:
        """Collect top-level PR conversation comments from one repository scan."""
        if not pr_numbers:
            return []
        extra: dict[str, object] = {"sort": "created", "direction": "asc"}
        if since:
            extra["since"] = since
        raw = self._paged(f"/repos/{repo}/issues/comments", extra=extra)
        comments: list[ReviewComment] = []
        for item in raw:
            pr_number = _number_from_api_url(item.get("issue_url"))
            if pr_number not in pr_numbers:
                continue
            user = item.get("user") or {}
            comments.append(
                ReviewComment(
                    repo=repo,
                    pr_number=pr_number,
                    url=item.get("html_url") or item.get("url") or "",
                    author=user.get("login") or "unknown",
                    author_type=user.get("type"),
                    body=item.get("body") or "",
                    path=None,
                    created_at=item.get("created_at"),
                    author_association=item.get("author_association"),
                )
            )
        return comments

    def selected_pull_request_comments(
        self,
        repo: str,
        *,
        pr_numbers: set[int],
        issue_comments: bool = False,
    ) -> list[ReviewComment]:
        """Read only the selected PRs when a single old PR widens the time window.

        Recently updated/merged PRs can have creation dates many years in the
        past. A repository-wide ascending scan from that date can be huge and
        truncated; fetching each selected PR avoids the correctness hazard.
        """
        collection = "issues" if issue_comments else "pulls"
        comments: list[ReviewComment] = []
        for number in sorted(pr_numbers):
            raw = self._paged(
                f"/repos/{repo}/{collection}/{number}/comments",
                max_pages=10,
            )
            for item in raw:
                user = item.get("user") or {}
                comments.append(
                    ReviewComment(
                        repo=repo,
                        pr_number=number,
                        url=item.get("html_url") or item.get("url") or "",
                        author=user.get("login") or "unknown",
                        author_type=user.get("type"),
                        body=item.get("body") or "",
                        path=None if issue_comments else item.get("path"),
                        created_at=item.get("created_at"),
                        author_association=item.get("author_association"),
                    )
                )
        return comments

    def collect(self, repo: str, *, max_prs: int = 100, include_issue_comments: bool = False) -> list[ReviewComment]:
        pulls = self.merged_pull_requests(repo, max_prs=max_prs)
        if not pulls:
            return []

        pr_numbers = {int(pull["number"]) for pull in pulls}
        created_at_values = [pull.get("created_at") for pull in pulls if pull.get("created_at")]
        since = min(created_at_values) if created_at_values else None

        # One PR merged today may have been opened years ago. Restricting the
        # scan by that PR's creation date makes repository-wide pagination
        # prohibitively expensive or incomplete on active projects.
        oldest = datetime.fromisoformat(since.replace("Z", "+00:00")) if since else None
        per_pr = bool(oldest and datetime.now(timezone.utc) - oldest > timedelta(days=90))
        if per_pr:
            comments = self.selected_pull_request_comments(repo, pr_numbers=pr_numbers)
            if include_issue_comments:
                comments.extend(
                    self.selected_pull_request_comments(
                        repo, pr_numbers=pr_numbers, issue_comments=True
                    )
                )
        else:
            comments = self.repository_review_comments(repo, pr_numbers=pr_numbers, since=since)
            if include_issue_comments:
                comments.extend(self.repository_issue_comments(repo, pr_numbers=pr_numbers, since=since))
        return comments
