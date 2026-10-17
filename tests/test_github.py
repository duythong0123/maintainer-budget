import unittest
from unittest.mock import patch

from maintainer_budget.github import GitHubClient, _number_from_api_url


class FakeGitHubClient(GitHubClient):
    def __init__(self):
        super().__init__(token="test")
        self.calls = []

    def _get(self, path, params=None):
        self.calls.append((path, params or {}))
        if path.endswith("/pulls/comments"):
            return [
                {
                    "pull_request_url": "https://api.github.com/repos/o/r/pulls/11",
                    "html_url": "https://github.com/o/r/pull/11#discussion_r1",
                    "user": {"login": "alice", "type": "User"},
                    "body": "Please use WidgetFactory::default().",
                    "path": "src/a.py",
                    "created_at": "2026-10-02T00:00:00Z",
                    "author_association": "MEMBER",
                },
                {
                    "pull_request_url": "https://api.github.com/repos/o/r/pulls/999",
                    "html_url": "https://github.com/o/r/pull/999#discussion_r2",
                    "user": {"login": "mallory", "type": "User"},
                    "body": "Unrelated comment.",
                    "path": "src/x.py",
                    "created_at": "2026-10-03T00:00:00Z",
                    "author_association": "MEMBER",
                },
                {
                    "pull_request_url": "https://api.github.com/repos/o/r/pulls/10",
                    "html_url": "https://github.com/o/r/pull/10#discussion_r3",
                    "user": {"login": "bob", "type": "User"},
                    "body": "Use WidgetFactory::default() here too.",
                    "path": "src/b.py",
                    "created_at": "2026-10-04T00:00:00Z",
                    "author_association": "COLLABORATOR",
                },
            ]
        if path.endswith("/issues/comments"):
            return [
                {
                    "issue_url": "https://api.github.com/repos/o/r/issues/10",
                    "html_url": "https://github.com/o/r/pull/10#issuecomment-1",
                    "user": {"login": "bob", "type": "User"},
                    "body": "Please keep the fixture convention.",
                    "created_at": "2026-10-05T00:00:00Z",
                    "author_association": "COLLABORATOR",
                },
                {
                    "issue_url": "https://api.github.com/repos/o/r/issues/777",
                    "html_url": "https://github.com/o/r/issues/777#issuecomment-2",
                    "user": {"login": "other", "type": "User"},
                    "body": "Not part of the audit.",
                    "created_at": "2026-10-05T00:00:00Z",
                    "author_association": "MEMBER",
                },
            ]
        raise AssertionError(f"unexpected path: {path}")


class GitHubClientTests(unittest.TestCase):
    def test_extracts_number_from_api_url(self):
        self.assertEqual(_number_from_api_url("https://api.github.com/repos/o/r/pulls/42"), 42)
        self.assertEqual(_number_from_api_url("https://api.github.com/repos/o/r/issues/7/"), 7)
        self.assertIsNone(_number_from_api_url(None))
        self.assertIsNone(_number_from_api_url("not-a-number"))

    def test_collect_batches_review_comments_and_filters_to_target_prs(self):
        client = FakeGitHubClient()
        pulls = [
            {"number": 11, "created_at": "2026-10-01T00:00:00Z", "merged_at": "2026-10-06T00:00:00Z"},
            {"number": 10, "created_at": "2026-09-20T00:00:00Z", "merged_at": "2026-10-05T00:00:00Z"},
        ]
        with patch.object(client, "merged_pull_requests", return_value=pulls):
            comments = client.collect("o/r", max_prs=2)

        self.assertEqual([c.pr_number for c in comments], [11, 10])
        self.assertEqual(len(client.calls), 1)
        path, params = client.calls[0]
        self.assertEqual(path, "/repos/o/r/pulls/comments")
        self.assertEqual(params["since"], "2026-09-20T00:00:00Z")
        self.assertEqual(params["sort"], "created")
        self.assertEqual(params["direction"], "asc")

    def test_optional_issue_comments_use_one_repository_scan(self):
        client = FakeGitHubClient()
        pulls = [
            {"number": 10, "created_at": "2026-09-20T00:00:00Z", "merged_at": "2026-10-05T00:00:00Z"},
        ]
        with patch.object(client, "merged_pull_requests", return_value=pulls):
            comments = client.collect("o/r", max_prs=1, include_issue_comments=True)

        self.assertEqual([c.pr_number for c in comments], [10, 10])
        self.assertEqual(
            [path for path, _ in client.calls],
            ["/repos/o/r/pulls/comments", "/repos/o/r/issues/comments"],
        )

    def test_no_merged_pulls_makes_no_comment_requests(self):
        client = FakeGitHubClient()
        with patch.object(client, "merged_pull_requests", return_value=[]):
            comments = client.collect("o/r", max_prs=100)
        self.assertEqual(comments, [])
        self.assertEqual(client.calls, [])


if __name__ == "__main__":
    unittest.main()
