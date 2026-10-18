# Launch kit

Maintainer Budget should be promoted with the same rule it applies to repository memory: **claims need evidence**.

Do not inflate stars, usage, precision, or adoption. Link to the public pilot scorecard when numbers exist.

## One-line pitch

> Maintainer Budget finds recurring human code-review feedback and turns it into evidence-backed repository rule candidates for maintainers and coding agents.

## GitHub / social short pitch

> Stop reviewing the same mistake twice. Maintainer Budget mines merged PR review history for recurring human feedback, preserves the original evidence, and proposes repository-specific rules for human approval. No API key, server, database, or code execution required.

## Hacker News title

`Show HN: Maintainer Budget – turn repeated code-review feedback into repository memory`

## Hacker News body

Maintainers often repeat the same repository-specific feedback across pull requests, while new contributors and coding agents do not know the convention yet.

Maintainer Budget is a small read-only GitHub Action/CLI that looks for recurring human review feedback across merged PRs and emits candidate repository rules with links back to the original comments.

The core intentionally uses no paid model/API, database, or server. Bot comments are ignored by default and nothing is written to AGENTS.md automatically. The maintainer still accepts, edits, rejects, or marks a rule stale.

A focused regression fixture from openai/codex uses two real review comments about the V2 `camelCase` convention; the first lexical baseline missed the pair, so the current alpha added identifier anchors while preserving the original evidence.

I am looking for public OSS repositories with meaningful review history for a small pilot. False positives are useful data and stay in the public scorecard.

Repo: https://github.com/duythong0123/maintainer-budget
Pilot: https://github.com/duythong0123/maintainer-budget/issues/3

## Reddit / maintainer community body

I built a tiny GitHub Action to answer a specific maintainer question: **what feedback have we already had to repeat across PRs?**

It reads merged PR review comments, filters for likely actionable human feedback, clusters recurring signals, and keeps direct links to the evidence. It does not execute repository code and does not require an AI key.

The project is deliberately conservative because a noisy rule generator would create more review work, not less. The first pilot is measuring ACCEPT / EDIT / REJECT / STALE verdicts, with false positives kept in the denominator.

If you maintain a public repo with active code review, I would value a report review more than a star: https://github.com/duythong0123/maintainer-budget/issues/3

## OpenAI / agent-developer community pitch

Coding agents can follow repository instructions, but maintainers first have to identify which local conventions deserve to become durable instructions.

Maintainer Budget mines recurring **human** review feedback, preserves provenance, and produces evidence bundles that can be semantically refined by Codex without making Codex the source of policy. The intended loop is:

```text
human review history
  → evidence-backed candidate
  → optional Codex deduplication/scoping
  → human approval
  → AGENTS.md / scoped repository instructions
```

The default core remains deterministic and dependency-light; Codex is an optional semantic layer where lexical matching is insufficient.

## Pilot outreach template

> Hi — I am validating a small OSS tool called Maintainer Budget. It reads public merged-PR review history and looks for feedback maintainers have had to repeat. It is read-only, ignores bots by default, executes no repo code, and requires no API key. Would you be willing to inspect a few evidence-backed candidates from your repo and mark them ACCEPT / EDIT / REJECT / STALE? Bad results are useful and are tracked publicly. https://github.com/duythong0123/maintainer-budget

## Launch gate

Before broad promotion:

- `main` CI is green;
- quickstart uses the stable rolling `@v0` Action ref;
- focused `openai/codex` regression is documented;
- public pilot and scorecard are open;
- at least one external maintainer has reviewed real output, or the launch post clearly says the pilot is seeking the first external repositories.

Do not claim an acceptance rate until human-labeled pilot data exists.

## Public launch wave 1 — 2026-10-18

**Headline:** `Show HN: I mined 367 Next.js review comments to find rules — the first rule was wrong`

**Copy-ready body (present tense, no adoption claims):**

> I built Maintainer Budget, a tiny read-only GitHub Action that looks for recurring *human* review feedback across merged PRs. The aim is to surface repository-specific rule candidates with links back to the comments, not to generate policy from thin air.
>
> The first live Next.js evaluation collected 367 review comments and identified 51 likely actionable human comments. It proposed one recurring rule — but it was a false positive: two unrelated comments shared the phrase `follow-up`. I turned those comments into a regression test and tightened identifier matching. In a smaller post-fix live run, the same false positive was gone (37 comments, 6 actionable, 0 candidates). Those are different windows; this is a bugfix demonstration, not a claim of benchmark precision.
>
> It requires no paid model, backend, database or custom secret when run as an Action in your own repository. It ignores bots by default and never changes `AGENTS.md` automatically.
>
> I am looking for 5–10 OSS maintainers willing to look at reports and mark proposed rules ACCEPT / EDIT / REJECT / STALE, including bad results. No external pilots or success rate are claimed yet.
>
> Repo: https://github.com/duythong0123/maintainer-budget
>
> Live public run: https://github.com/duythong0123/maintainer-budget/actions/workflows/public-demo.yml
>
> Pilot signup: https://github.com/duythong0123/maintainer-budget/issues/3

**Short social version:**

> Reviewing the same repository convention repeatedly is expensive. I made a GitHub Action to find repeated *human* PR review feedback and preserve evidence links. A live Next.js run found a false rule; that false positive is now a regression test. Looking for early maintainer pilots, especially people willing to report bad output. https://github.com/duythong0123/maintainer-budget

**Status:** these are publication-ready drafts **not yet posted** to Hacker News, Reddit, or social networks. Do not claim otherwise. See [`docs/distribution-wave-1.md`](distribution-wave-1.md) for targeted outreach and curated list contribution instructions.
