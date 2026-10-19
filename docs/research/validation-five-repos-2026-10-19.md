# Five-repository validity check — 2026-10-19

**Decision: evidence of a real use case, but not enough precision or maintainer validation to launch broadly.**

This is an **internal engineering assessment** of public OSS review history, **not** an independent pilot, customer endorsement, externally validated useful rate, or OpenAI funding evidence.

## Reproducible run

- [Five-repo GitHub Actions run #39213532206](https://github.com/duythong0123/maintainer-budget/actions/runs/39213532206) — **all five matrix jobs completed successfully**.
- [Research workflow](https://github.com/duythong0123/maintainer-budget/blob/research/validation-2026-10-19/.github/workflows/validation-five-repos.yml): real current `maintainer-budget audit` CLI, `--max-prs 100`, default similarity `0.34`, minimum two distinct PRs, **inline pull-request review comments only** (top-level issue comments not included).
- Selection: up to 100 merged PRs per repository drawn from GitHub's **closed PR list ordered by most recently updated**, not necessarily the 100 most recently *merged* by merge timestamp. The CLI's `human_actionable_comments` statistic is **heuristic filtering**, not human-validated actionable labels.
- Public target repositories were read-only; no target repo code executed or modified. Each matrix job published a Markdown report, JSON evidence, and share card (30-day artifact retention).
- Collection correction included in the experiment: a newly merged PR could have been created years ago (e.g. a selected pytest PR from 2020). For wide time ranges, the collector now fetches only the selected PRs' review endpoints; hitting its pagination ceiling fails explicitly rather than silently returning partial data. Transient 502/503/504 errors receive limited retries.
- A preliminary **50-PR** run had 502 errors on pytest and ruff and is **not used as the benchmark**. The successful 100-PR run below is the basis for these totals.

## Raw CLI outputs

| Repository | Merged PR limit | Review comments | Heuristically actionable human comments | Candidate groups |
| --- | ---: | ---: | ---: | ---: |
| [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | 100 | 339 | 80 | 1 |
| [vitest-dev/vitest](https://github.com/vitest-dev/vitest) | 100 | 68 | 16 | 0 |
| [astral-sh/ruff](https://github.com/astral-sh/ruff) | 100 | 245 | 101 | 0 |
| [Textualize/textual](https://github.com/Textualize/textual) | 100 | 53 | 6 | 0 |
| [az-digital/az_quickstart](https://github.com/az-digital/az_quickstart) | 100 | 121 | 29 | 2 |
| **Total** | **500** | **826** | **232** | **3** |

Counts from the `VALIDATION_STATS` lines in the jobs' public logs and machine-readable artifact reports. Candidate counts are raw model-free lexical clustering output, not accepted rules.

## Manual engineering assessment of *all three* candidate groups

### az_quickstart MB-002 — promising recurring human review **(not maintainer-approved)**

The *same* reviewer, `tadean`, repeats almost the same guidance on **two different merged PRs**:

- [PR #5990](https://github.com/az-digital/az_quickstart/pull/5990#discussion_r4008951885): “Should this be an OOP hook rather than procedural?”
- [PR #6021](https://github.com/az-digital/az_quickstart/pull/6021#discussion_r4107056194): “Should this be an OOP hook rather than a procedural one?”

CLI cluster score **0.881**; 2 PRs, 1 reviewer. **Provisional engineering judgment: plausible useful repo-specific review signal.** It is still a *question*, not proof the repo always prefers OOP hooks. Maintainers must confirm whether the convention should be included, narrowed, or rejected. This independently matches the same pair discovered by manual scouting before the audit.

We already provided the two citations in [the repo's AGENTS.md review-guidance issue #6077](https://github.com/az-digital/az_quickstart/issues/6077#issuecomment-6247373080); **do not post a repeat solicitation**. No maintainer response or verdict yet.

### az_quickstart MB-001 — likely false positive

Three unrelated comments were linked by recurring `az_*` module names in different contexts:

- [PR #5958](https://github.com/az-digital/az_quickstart/pull/5958#discussion_r3991798797) — logger label `az_barrio` vs `az_quickstart`
- [PR #5966](https://github.com/az-digital/az_quickstart/pull/5966#discussion_r3970848048) — where a tooltip JS library should live
- [PR #5997](https://github.com/az-digital/az_quickstart/pull/5997#discussion_r4028587280) — lifecycle of `az_core` service

CLI score **0.078**, 3 PRs, 3 reviewers. Shared identifiers **do not imply the same instruction**. **Provisional engineering judgment: likely reject/no single actionable policy**.

### pytest MB-001 — too generic / likely false positive

- [PR #14758](https://github.com/pytest-dev/pytest/pull/14758#discussion_r3637005330) — keep code simple because performance is not a problem
- [PR #14865](https://github.com/pytest-dev/pytest/pull/14865#discussion_r3789353601) — simplify Linux-conditional implementation

CLI score **0.349**, 2 PRs, 1 reviewer. **Provisional engineering judgment: likely reject for repository-memory export**: the shared phrase “keep the code simple” is general advice, with two distinct technical rationales; it is not a concrete repository-specific convention.

## Interpretation and next product decision

- **1 plausible / 3 total** surfaced groups based on this *internal* examination. Two are likely false positives. This is **not** a product precision estimate or a maintainer-labeled useful rate; sample size is tiny and source selection non-random.
- **0 verified external pilots; 0 actual maintainer `ACCEPT/EDIT/REJECT/STALE` labels.** The pilot scorecard must stay at zero.
- **Do not increase automation or claim 80% accuracy.** Avoid promoting empty audits as successes.
- **Product direction:** prioritize an *evidence-first*, human-approved review memory tool; improve candidate grouping to require the *same requested change or convention*, not merely a shared identifier or generic phrase. Preserve evidence and empty reports. Evaluate broader and varied review histories before another distribution push.
- **User research:** wait for an authentic reply to [az_quickstart #6077](https://github.com/az-digital/az_quickstart/issues/6077); if a maintainer responds, show the specific candidate and ask whether they would have wanted it surfaced, without requiring installation first. Until then this is **an observed problem**, not validated user demand.

## Raw artifacts

The successful [run #39213532206](https://github.com/duythong0123/maintainer-budget/actions/runs/39213532206) contains five artifacts:
`validation-pytest`, `validation-vitest`, `validation-ruff`, `validation-textual`, `validation-az_quickstart`. Each includes full Markdown/JSON evidence and a share card. Artifacts expire after 30 days; URLs to original review discussions remain available.
