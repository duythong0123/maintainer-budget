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
