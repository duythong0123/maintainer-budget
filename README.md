# Maintainer Budget

> **Stop reviewing the same mistake twice.**

Maintainer Budget turns repeated **human code-review feedback** into **evidence-backed repository rule candidates** that maintainers can inspect before adding them to `AGENTS.md` or other agent instructions.

It is built around one problem: important project conventions often live in maintainer heads and old PR threads. New contributors — and coding agents — miss those conventions, so maintainers spend attention repeating the same review.

```text
PR #142  “Use the service layer here.”
PR #181  “API handlers should not call the DB directly.”
PR #247  “Please route this through UserService.”
                         ↓
                Maintainer Budget
                         ↓
Candidate MB-001
“API handlers should use the service layer for database access.”

Evidence: #142 · #181 · #247
Status: candidate — human approval required
```

## Why this is different

Maintainer Budget is **not** another AI code reviewer and it does not try to detect “AI code”. The alpha is deliberately conservative:

- no paid API required;
- bot comments are ignored by default;
- no contributor code is executed;
- a candidate must recur across different PRs;
- the candidate text comes from real human review feedback;
- every candidate keeps direct links to its evidence;
- nothing becomes repository policy automatically.

The goal is repository memory with provenance, not plausible-sounding rules.

## Fastest way to try it: GitHub Action

Create `.github/workflows/maintainer-budget.yml` in your repository:

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
      - uses: duythong0123/maintainer-budget@main
        with:
          max-prs: "100"
```

Run the workflow manually from **Actions → Maintainer Budget → Run workflow**. The action uses the repository's built-in `GITHUB_TOKEN`, audits merged PR review history, and uploads four small files:

- `maintainer-budget.md` — full human-readable report;
- `maintainer-budget.json` — machine-readable evidence;
- `maintainer-budget-share.md` — compact copy/paste summary for issues, README discussions, or launch posts;
- `maintainer-budget-codex.md` — optional evidence bundle for Codex semantic review.

The copy-paste example also lives in [`examples/maintainer-budget.yml`](examples/maintainer-budget.yml).

> Alpha note: `@main` is used until the first stable action tag is cut. Pin a release tag once one is available.

## Alpha CLI

Install directly from GitHub:

```bash
python -m pip install "git+https://github.com/duythong0123/maintainer-budget.git"
maintainer-budget audit openai/codex --max-prs 100
```

For higher GitHub API rate limits, set `GITHUB_TOKEN` or `GH_TOKEN`.

Write all lightweight outputs in one pass:

```bash
maintainer-budget audit owner/repo \
  --max-prs 200 \
  --output maintainer-budget.md \
  --json maintainer-budget.json \
  --share-card maintainer-budget-share.md \
  --codex-bundle maintainer-budget-codex.md
```

The full output contains candidate rules plus the PR, reviewer, path, comment excerpt, and source URL for each piece of evidence.

## Optional Codex workflow — no SDK required

The core remains dependency-free. `--codex-bundle` does **not** call an API; it creates a strict evidence packet that can be handed to Codex when a maintainer wants semantic help.

The bundle tells Codex to:

- never invent repository policy;
- preserve candidate IDs and original evidence URLs;
- merge paraphrases only when the evidence supports the same convention;
- mark ambiguous or stale candidates for human review;
- never edit `AGENTS.md` automatically.

This keeps the default install tiny while making Codex useful exactly where deterministic clustering starts to struggle.

## Shareable result

`maintainer-budget-share.md` is intentionally short enough to paste into an issue or post:

```text
Maintainer Budget · owner/repo

1,284 review comments · 312 actionable human comments · 18 recurring candidates

MB-001 · 7 PRs · 3 reviewers — Use the service layer for database access...
MB-002 · 5 PRs · 2 reviewers — Generated files should not be edited manually...
MB-003 · 4 PRs · 2 reviewers — Migrations require rollback logic...
```

The numbers are observed data, not an AI quality score.

## How it works

```text
GitHub merged PR history
        ↓
review comments from humans
        ↓
filter likely actionable feedback
        ↓
deterministic similarity clustering
        ↓
repo-specific identifier anchors
        ↓
require recurrence across distinct PRs
        ↓
rank candidates + preserve provenance
        ↓
optional Codex semantic review
        ↓
human ACCEPT / EDIT / REJECT / STALE
```

The alpha uses a small TF-IDF/cosine baseline from the Python standard library plus exact anchors for stable repository-specific identifiers such as `camelCase`, `nextTestSetup`, `_register`, or `ConfigBuilder::default`. This is intentionally less “smart” than an LLM: it gives the project an auditable benchmark before an optional semantic layer is used.

## Real-data regression demo

Two public `openai/codex` review comments describe the same convention using very different prose:

```text
PR #6467
“we are using camelCase throughout the V2 protocol...”

PR #8442
“add #[serde(rename_all = \"camelCase\")]...”
```

The first TF-IDF baseline missed this pair. The current alpha links them through the stable `camelCase` identifier and emits one evidence-backed candidate spanning two PRs.

See [`research/demo-openai-codex.md`](research/demo-openai-codex.md) for the exact public evidence and current output.

## Example candidate

```text
MB-001

Candidate rule
──────────────
FYI, we are using "camelCase" throughout the V2 protocol,
so let's follow suit here.

Unique PRs: 2
Unique reviewers: 1
Shared signal: camelcase
Evidence:
- PR #6467 · codex-rs/execpolicy2/src/decision.rs
- PR #8442 · codex-rs/network-proxy/src/config.rs
```

A maintainer should **accept, edit, or reject** the candidate. Automatic `AGENTS.md` modification is intentionally not part of the first alpha.

## Validation so far

Initial public-data checks found promising recurring repository-specific signals in `openai/codex`, `vercel/next.js`, and `microsoft/vscode`. The notes and limitations are documented in [`research/validation.md`](research/validation.md).

The metric that matters next is **candidate acceptance rate**, not stars or number of generated rules.

## Roadmap

- **0.1 alpha** — read-only GitHub audit + deterministic candidate clustering + zero-setup GitHub Action + share/Codex exports.
- **0.1 beta** — explicit accept/edit/reject decisions and controlled `AGENTS.md` export.
- **0.3** — backtest candidate rules against historical PRs; detect stale rules.
- **0.4** — optional deeper Codex semantic layer for paraphrases, always evidence-bound and human-approved.
- **1.0** — stable rule schema + documented evaluation corpus.

See [`docs/design.md`](docs/design.md).

## Contributing

The most valuable contribution is a real example of a candidate that is useful, misleading, duplicated, or stale. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Security

Maintainer Budget only reads GitHub metadata/comments in the alpha and never executes code from the target repository. See [`SECURITY.md`](SECURITY.md).

## License

MIT.
