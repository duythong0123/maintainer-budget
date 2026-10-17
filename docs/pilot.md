# Maintainer Budget pilot

Maintainer Budget is looking for public open-source repositories with real pull-request review history to validate whether repeated maintainer feedback can be recovered as useful repository guidance.

## What the pilot is trying to learn

The project does **not** need more generated rules. It needs evidence about precision.

For each candidate, a maintainer labels it as one of:

- **ACCEPT** — useful as-is;
- **EDIT** — useful after a small edit or narrower scope;
- **REJECT** — noise, wrong, or too generic;
- **STALE** — historically valid but no longer current.

The primary metric is:

```text
useful rate = (ACCEPT + EDIT) / all reviewed candidates
```

We will also track stale candidates separately because historical review memory must not become permanent policy by accident.

## Pilot target

The first milestone is deliberately small:

- 5–10 public repositories;
- at least 30 human-labeled candidate clusters;
- evidence links preserved for every candidate;
- false positives documented, not hidden;
- target useful rate of at least 80% for high-confidence candidates before automatic `AGENTS.md` export is considered.

The 80% target is a product gate, not a claim that the current alpha already achieves it.

## How to participate

### Option A — GitHub Action

Add this workflow:

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

Run it manually and download the `maintainer-budget-report` artifact.

### Option B — CLI

```bash
python -m pip install "git+https://github.com/duythong0123/maintainer-budget.git"
maintainer-budget audit owner/repo --max-prs 100
```

Then open a **Candidate feedback** issue for candidates you inspect. Reporting a bad candidate is just as useful as reporting a good one.

## Safety and scope

The alpha is read-only. It does not execute code from the audited repository, does not require a paid AI API, and does not automatically modify repository policy.

Public pilot results should be aggregate and evidence-backed. The goal is to improve the tool, not rank contributors or reviewers.
