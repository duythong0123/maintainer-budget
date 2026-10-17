# Live evaluation: `vercel/next.js`

This page documents both **ecosystem evidence** and a **real Maintainer Budget live run**. The benchmark is engineering validation, not external adoption and not a claim that Next.js maintainers endorse the project.

## Human review signal

In [PR #99195](https://github.com/vercel/next.js/pull/99195), maintainer `@gnoff` left a focused review comment:

> should we just use `@force-gate !dev` instead?

The author changed the PR accordingly and explained that the static gate is resolved at collection time rather than through the older mode-check pattern.

This is exactly the kind of knowledge a new contributor or coding agent is unlikely to infer from generic TypeScript/Jest knowledge alone: it is a convention of the Next.js test harness.

## Agent-instruction signal

In [PR #99582](https://github.com/vercel/next.js/pull/99582), Codex reviewed a test gate and explicitly cited `test/AGENTS.md` while arguing that a suite-level `@force-gate` would hide deployed behavior that should remain visible.

That is useful product evidence for this loop:

```text
historical maintainer feedback
        ↓
repository-specific rule candidate
        ↓
human approval
        ↓
AGENTS.md / scoped instructions
        ↓
agent review can apply the rule later
```

The Codex comment is **not** used as human training evidence by the alpha; bot feedback is ignored by default. It is included here only as public evidence that repository instructions can materially affect an agent review.

## Live alpha run: the useful failure

The first public live audit used a recent 60-merged-PR window from `vercel/next.js`.

```text
Review comments collected:       367
Likely actionable human comments: 51
Recurring candidates:              1
```

The only candidate was wrong. It joined two unrelated review comments because both contained the ordinary English phrase `follow-up`:

- [PR #98469 review](https://github.com/vercel/next.js/pull/98469#discussion_r3983819642)
- [PR #98932 review](https://github.com/vercel/next.js/pull/98932#discussion_r4163950930)

The comments were about different code and different decisions. `follow-up` was not a repository convention.

We kept this result visible instead of removing it from the evaluation story. PR #14 added those exact public comments as a regression test and changed anchor detection so plain hyphenated prose is no longer treated like a stable repository identifier. Code-shaped identifiers such as `camelCase`, `_register`, dotted names and `ConfigBuilder::default` remain eligible; hyphenated/kebab identifiers can still be anchors when reviewers explicitly format them as code.

## Post-fix compact run

The recurring public demo intentionally uses a much smaller recent window because cross-repository calls from GitHub-hosted runners use the anonymous public API and share a low rate limit.

Post-fix output:

```text
Review comments collected:        37
Likely actionable human comments:  6
Recurring candidates:              0
```

The false `follow-up` cluster no longer appears.

For this alpha, **zero candidates is a valid result**. Returning no rule is preferable to turning plausible prose into unsupported repository policy.

The recurring workflow is in [`.github/workflows/public-demo.yml`](../.github/workflows/public-demo.yml), and the public validation totals remain tracked in [scorecard #4](https://github.com/duythong0123/maintainer-budget/issues/4).

## Why this matters

Next.js has its own concepts such as `@gate`, `@force-gate`, deploy-mode behavior, and fixture lifecycle. A generic reviewer can understand JavaScript and Jest while still missing those local invariants.

Maintainer Budget's goal is to recover the recurring human feedback that reveals such invariants, preserve the original evidence, and let maintainers decide which ones deserve to become durable repository instructions. The live run also demonstrates the project's evaluation rule: false positives become regression tests instead of marketing claims.
