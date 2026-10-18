# Distribution wave 1 — 2026-10-18

This is a practical launch and outreach packet for the alpha. **Drafted / identified is not sent, accepted, adopted or endorsed.** Public scorecard: https://github.com/duythong0123/maintainer-budget/issues/4

## First contact targets (candidate pilot repositories)

Selection criteria: public OSS, recent merged PRs with verifiable human feedback, and plausible value from persistent repo-specific conventions. These repositories have **not agreed** to a pilot. We should approach them with a single respectful request where appropriate, not file promotional issues on their repositories.

| Priority | Repository | Public human-review evidence | Why this might fit | State |
| --- | --- | --- | --- | --- |
| 1 | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | [PR #15040](https://github.com/pytest-dev/pytest/pull/15040) — a reviewer calls out a namespace-package edge case, followed by an author response | Complex long-lived testing conventions and repeated contributor feedback | Not contacted |
| 2 | [Textualize/textual](https://github.com/Textualize/textual) | [PR #6543](https://github.com/Textualize/textual/pull/6543) — reviewer explains a keyboard shortcut conflict with the command palette | UI/keybinding conventions often live in review threads | Not contacted |
| 3 | [vitest-dev/vitest](https://github.com/vitest-dev/vitest) | [PR #11407](https://github.com/vitest-dev/vitest/pull/11407) — a human reviewer debates JUnit escaping semantics | Test-reporter conventions and compatibility knowledge across PRs | Not contacted |
| 4 | [pydantic/pydantic](https://github.com/pydantic/pydantic) | [PR #14008](https://github.com/pydantic/pydantic/pull/14008) contains bot noise alongside human participation | Schema/compatibility conventions; bot filtering is critical | Not contacted |
| 5 | [astral-sh/ruff](https://github.com/astral-sh/ruff) | [PR #29429](https://github.com/astral-sh/ruff/pull/29429) shows heavy automation and a human review submission | Potential high-volume case; use only after identifying richer human comments | Not contacted |

These are **fit signals**, not evidence that the current alpha has found recurring rules in these repositories. Do not count them as pilot users or candidate labels.

## First outreach message (public comment only if invited or on an appropriate project discussion)

> Hi! I'm validating a small OSS GitHub Action called [Maintainer Budget](https://github.com/duythong0123/maintainer-budget). It reads public merged-PR review history and looks for review feedback humans have had to repeat, with direct evidence links. It does not execute repository code, modify policy, or require a paid API. I noticed your repository has substantive human reviews (e.g. the linked PR above), so I wondered if you would be interested in *reviewing* an audit output. Even an empty or incorrect result is helpful. You would only need to inspect candidates and optionally mark ACCEPT / EDIT / REJECT / STALE. No pressure; details at [pilot #3](https://github.com/duythong0123/maintainer-budget/issues/3).

Do not assert affiliation, endorsement, or maintainer approval. Avoid @-mention spam. One invitation per maintainer/channel, no automated follow-up without permission.

## Curated GitHub Actions list submission

Target: https://github.com/sdras/awesome-actions

Read contribution rules: https://github.com/sdras/awesome-actions/blob/main/contributing.md

The most suitable existing category is **Pull Requests** (the product mines PR review history). Add one item **at the end of that category**, not as a new category and not in Static Analysis:

`- [Maintainer Budget](https://github.com/duythong0123/maintainer-budget) - Find recurring human code-review feedback and preserve evidence-backed rule candidates.`

Proposed PR title: `Add Maintainer Budget to Pull Requests tools`

Proposed commit message: `docs: list Maintainer Budget GitHub Action`

Proposed PR body:
> Adds [Maintainer Budget](https://github.com/duythong0123/maintainer-budget), a read-only GitHub Action that mines repeated human PR-review feedback into evidence-backed repository-rule candidates. It is published on GitHub Marketplace, has a documented live OSS evaluation, and requires no paid AI API. One entry, in the Pull Requests category, following the list's contribution guidelines.

**Status: not submitted.** The connected GitHub integration can edit the owned repo, but no fork-creation action is available; the account has no `duythong0123/awesome-actions` fork yet. Do not claim a submitted PR.

## First wave checkpoints

| Work item | Status |
| --- | --- |
| Public alpha release + Marketplace | Done |
| Repo description and topics | Done |
| Evidence-backed launch copy | Prepared in `docs/launch.md` |
| Pilot contact shortlist | Identified, 0 contacted |
| Awesome Actions PR | Prepared, not submitted |
| External pilot repositories | 0 confirmed |
| Human-labeled candidate clusters | 0 confirmed |
| Github stars | 0 at baseline on 2026-10-18 |

Only update externally verified figures. The next substantive evidence is a maintainer actually replying or a repo owner submitting a report, not the number of drafts.

## Community launch priority update — 2026-10-18

**First external post target:** [r/github self-promotion megathread](https://www.reddit.com/r/github/comments/1jy8rea/promote_your_projects_here_selfpromotion/). That thread explicitly invites GitHub project posts. Recheck current pinned threads and subreddit rules when posting.

**Suggested short comment (owner should personalize in their own voice):**

> I'm testing an open-source GitHub Action called Maintainer Budget. It looks through merged pull-request reviews for feedback human reviewers have repeated across different PRs, and produces evidence-linked candidates rather than changing repo policy automatically.
>
> A public Next.js trial uncovered a false positive: two unrelated reviews both used `follow-up`. I added a regression test and tightened the matcher. The next smaller run produced zero candidates, which is fine for a conservative alpha.
>
> I would appreciate feedback from maintainers with active PR review history; false positives and empty reports are useful too. No paid API key, DB or backend needed: https://github.com/duythong0123/maintainer-budget . Pilot instructions: https://github.com/duythong0123/maintainer-budget/issues/3

**Status:** drafted, **not posted**. Posting requires the repo owner's Reddit account; the connected GitHub integration cannot post to Reddit.

**Show HN:** [official HN announcement](https://news.ycombinator.com/showlim) currently says Show HNs are temporarily restricted for unfamiliar accounts; [submission guidelines](https://news.ycombinator.com/newsguidelines.html) also discourage automated/AI-written posts and promotional-only accounts. Hold the prepared draft and do not post it verbatim or via automation.

**awesome-actions:** [contribution guidelines](https://github.com/sdras/awesome-actions/blob/main/contributing.md) allow one-entry PRs, but the repo has a large open-PR backlog; treat this as a secondary discovery channel rather than the route to immediate pilots. A fork is not currently available and the connected GitHub App uses **selected-repository** access, so creating a fork alone may not authorize assistant writes there. A human account owner would need to fork and possibly grant the app access, or submit the PR via GitHub UI.

Next measurable outcome: the first authentic external outreach message/post or maintainer feedback link. Until then: **0 posts, 0 contacts, 0 external pilots**.
