# GitHub Marketplace publication

This file is the source of truth for the first Marketplace listing. Keep public claims aligned with the pilot scorecard; do not claim adoption or precision before the data exists.

## Repository About metadata

**Description**

> Turn recurring human code-review feedback into evidence-backed repository rules for maintainers and coding agents.

**Topics**

```text
github-actions
code-review
open-source
maintainers
developer-tools
ai-agents
codex
agents-md
repository-memory
pull-requests
```

## Marketplace listing

Action metadata name: `Maintainer Budget Audit`

**Primary category:** Open Source management  
**Secondary category:** Code review

Rationale: the product manages durable maintainer knowledge recovered from review history; it is not a linter or a generic AI reviewer.

## First release

**Tag**

```text
v0.1.0-alpha.1
```

**Release title**

```text
Maintainer Budget v0.1.0-alpha.1 — Evidence before policy
```

Use the body from [`docs/releases/0.1.0a1.md`](releases/0.1.0a1.md).

Mark the release as **pre-release**.

When drafting the release from `action.yml`, select:

- `Publish this Action to the GitHub Marketplace`
- Primary category: `Open Source management`
- Secondary category: `Code review`

If GitHub asks for the Marketplace Developer Agreement, the repository owner must accept it before the publish checkbox can be enabled.

## Release target

Create the tag from the current green `main` commit, not from an older feature branch. The rolling `v0` branch should point to the same tested Action code or a newer compatible alpha commit.

## Listing copy

### Short description

> Recover recurring human review knowledge as evidence-backed repository rules — no API key, server, or database required.

### What it does

Maintainer Budget audits merged pull-request review history, filters for likely actionable human feedback, groups repeated repository-specific signals, and preserves direct links to the original review evidence. Maintainers keep control of ACCEPT / EDIT / REJECT / STALE decisions.

The Action is read-only, ignores bot feedback by default, executes no target-repository code, and can optionally produce a strict evidence bundle for Codex without requiring Codex or an OpenAI API key in the core workflow.

### Quickstart

```yaml
- uses: duythong0123/maintainer-budget@v0
  with:
    max-prs: "100"
```

The compact result appears directly in the GitHub Actions run summary; full Markdown, JSON, share-card, and Codex evidence files are also uploaded as artifacts.

## Publication checklist

- [x] public repository
- [x] one root `action.yml`
- [x] Action name, description, author, and branding
- [x] read-only default permissions documented
- [x] CI on Python 3.10 and 3.12
- [x] composite Action smoke test
- [x] README quickstart
- [x] MIT license
- [x] SECURITY.md
- [x] CONTRIBUTING.md
- [x] release notes
- [x] rolling `v0` Action ref
- [x] public pilot and scorecard
- [ ] repository About description/topics set in GitHub UI
- [ ] GitHub release/tag created
- [ ] Marketplace publish checkbox selected
- [ ] Marketplace Developer Agreement accepted if GitHub requests it

The final four items require repository-owner UI actions if the connected GitHub integration does not expose those settings.
