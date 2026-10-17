# Maintainer Budget

> **Stop reviewing the same mistake twice.**

Maintainer Budget mines repeated **human code-review feedback** and turns it into **evidence-backed repository rule candidates** for maintainers and coding agents.

**No API key. No server. No database. No contributor code execution.**

[![CI](https://github.com/duythong0123/maintainer-budget/actions/workflows/ci.yml/badge.svg)](https://github.com/duythong0123/maintainer-budget/actions/workflows/ci.yml)
[![Public OSS demo](https://github.com/duythong0123/maintainer-budget/actions/workflows/public-demo.yml/badge.svg)](https://github.com/duythong0123/maintainer-budget/actions/workflows/public-demo.yml)

## Try it in one workflow

Create `.github/workflows/maintainer-budget.yml`:

```yaml
name: Maintainer Budget

on:
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: read

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: duythong0123/maintainer-budget@v0
        with:
          max-prs: "100"
```

Run **Actions → Maintainer Budget → Run workflow**. The compact result appears directly in the GitHub Actions run summary, so you can judge the signal before downloading anything.

The action also uploads four small files:

- `maintainer-budget.md` — full evidence report;
- `maintainer-budget.json` — machine-readable data;
- `maintainer-budget-share.md` — compact summary for sharing;
- `maintainer-budget-codex.md` — optional evidence bundle for Codex.

`@v0` is the rolling alpha Action ref. Pin a commit SHA if you need an immutable dependency.

## What problem does this solve?

Important repository conventions often live in maintainers' heads and old PR threads:

```text
PR #142  "Use the service layer here."
PR #181  "API handlers should not call the DB directly."
PR #247  "Please route this through UserService."
                         ↓
                Maintainer Budget
                         ↓
Candidate MB-001
"API handlers should use the service layer for database access."

Evidence: #142 · #181 · #247
Status: candidate — human approval required
```

The goal is **repository memory with provenance**, not another plausible-sounding AI review.

## Real-data regression: `openai/codex`

Two public human review comments in `openai/codex` express the same repository convention with different prose:

```text
PR #6467
"we are using camelCase throughout the V2 protocol..."

PR #8442
"add #[serde(rename_all = \"camelCase\")]..."
```

The first TF-IDF baseline missed the relationship. The current alpha links them through the stable `camelCase` identifier and emits one evidence-backed candidate spanning two PRs.

See [`research/demo-openai-codex.md`](research/demo-openai-codex.md) for the exact public evidence and regression output.

## Live evaluation: false positives become tests

A real public audit of a recent `vercel/next.js` window collected **367 review comments**, retained **51 likely actionable human comments**, and emitted **1 candidate**. That candidate was wrong: two unrelated reviews were connected by the ordinary phrase `follow-up`.

We did not hide the result. The two exact public comments became a regression test, anchor detection was tightened in PR #14, and a post-fix compact live run returned:

```text
37 review comments
 6 actionable human comments
 0 recurring candidates
```

For a conservative alpha, zero candidates is better than unsupported repository policy. See [`research/demo-nextjs.md`](research/demo-nextjs.md) and the [public scorecard #4](https://github.com/duythong0123/maintainer-budget/issues/4). The [Public OSS demo workflow](https://github.com/duythong0123/maintainer-budget/actions/workflows/public-demo.yml) keeps exercising the core against public review history.

These runs are engineering validation, **not** external adoption or maintainer endorsement.

## Why this is different

Maintainer Budget is deliberately conservative:

- bot feedback is ignored by default;
- a candidate must recur across distinct PRs;
- candidate text comes from real human review feedback;
- every candidate keeps links to the original evidence;
- nothing becomes repository policy automatically;
- a maintainer still decides **ACCEPT / EDIT / REJECT / STALE**.

The alpha uses a dependency-free TF-IDF/cosine baseline plus stable repository-specific identifier anchors. An optional semantic layer can help later, but the core does not depend on an LLM.

## Optional Codex workflow

`--codex-bundle` creates a strict evidence packet for Codex. It does **not** call an API by itself.

The packet instructs Codex to preserve candidate IDs and evidence URLs, avoid inventing policy, merge paraphrases only when evidence supports the same convention, and return ambiguous or stale candidates to a human.

This creates a lightweight path from historical review knowledge to scoped agent instructions such as `AGENTS.md` without making the default install heavy.

Public evidence:

- [`openai/codex` focused regression](research/demo-openai-codex.md) — a real recurring `camelCase` convention used as a regression fixture;
- [`vercel/next.js` live evaluation](research/demo-nextjs.md) — a real public run, false positive, regression fix, and post-fix rerun;
- [`microsoft/vscode` instruction/lifecycle signal](research/demo-vscode.md) — why scope and provenance matter.

The VS Code page is landscape evidence, not a claim that the current alpha already produced those exact clusters.

## CLI

```bash
python -m pip install "git+https://github.com/duythong0123/maintainer-budget.git"
maintainer-budget audit openai/codex --max-prs 100
```

Write all outputs in one pass:

```bash
maintainer-budget audit owner/repo \
  --max-prs 200 \
  --output maintainer-budget.md \
  --json maintainer-budget.json \
  --share-card maintainer-budget-share.md \
  --codex-bundle maintainer-budget-codex.md
```

For higher GitHub API rate limits, set `GITHUB_TOKEN` or `GH_TOKEN`.

## How it works

```text
merged PR history
      ↓
human review comments
      ↓
actionable-feedback filter
      ↓
deterministic clustering
      ↓
repo-specific identifier anchors
      ↓
recurrence across distinct PRs
      ↓
evidence-backed candidates
      ↓
optional Codex semantic review
      ↓
human ACCEPT / EDIT / REJECT / STALE
```

## Pilot

The first public milestone is intentionally measurable:

- 5–10 public repositories;
- at least 30 human-labeled candidate clusters;
- original evidence preserved for every candidate;
- false positives kept in the denominator;
- target **≥80% ACCEPT + EDIT** useful rate for high-confidence candidates before automatic policy export is considered.

See [pilot recruitment #3](https://github.com/duythong0123/maintainer-budget/issues/3) and the [public scorecard #4](https://github.com/duythong0123/maintainer-budget/issues/4).

## Roadmap

- **v0 alpha** — read-only audit, deterministic clustering, GitHub Action, share card, Codex evidence bundle;
- **beta** — explicit candidate decisions and controlled instruction export;
- **later** — historical backtesting, stale-rule detection, optional deeper semantic matching;
- **1.0** — stable rule schema and public evaluation corpus.

See [`docs/design.md`](docs/design.md).

## Contributing

The most useful contribution is a real candidate that is useful, misleading, duplicated, or stale. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Security

The alpha reads GitHub metadata/review comments and never executes code from the audited repository. See [`SECURITY.md`](SECURITY.md).

## License

MIT.
