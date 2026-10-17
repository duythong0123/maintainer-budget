# Changelog

## 0.1.0a1 - 2026-10-17

First public alpha focused on one job: recover recurring **human** review knowledge without inventing repository policy.

### Core audit

- Read-only audit of recent merged GitHub pull requests.
- Filters bot feedback and low-trust review authors by default.
- Finds likely actionable human review feedback.
- Deterministic TF-IDF/cosine clustering across distinct PRs.
- Structured identifier anchors bridge paraphrased feedback around stable repo-specific symbols such as `camelCase` or `nextTestSetup`.
- Regression fixture from real `openai/codex` review comments (#6467 and #8442).

### Outputs

- Evidence-backed Markdown report.
- Machine-readable JSON report.
- Compact share card for issues/posts.
- Optional Codex evidence bundle with provenance and anti-hallucination constraints.
- GitHub Actions run summary shows the compact result immediately.

### Distribution

- Zero-setup composite GitHub Action.
- Rolling alpha Action ref: `duythong0123/maintainer-budget@v0`.
- CLI installable directly from GitHub.
- Runtime remains dependency-light: no database, server, or paid model/API required.

### Safety and product constraints

- Does not execute code from the audited repository.
- Does not automatically edit `AGENTS.md` or other repository policy.
- Candidate rules keep links to their source evidence.
- Human maintainers remain responsible for ACCEPT / EDIT / REJECT / STALE decisions.

### Known limitations

- Lexical clustering still misses semantic paraphrases that do not share a stable identifier.
- Candidate text is currently a real representative review comment rather than a synthesized polished rule.
- Precision is not yet claimed; the public pilot is collecting human labels before any acceptance-rate claim is made.
