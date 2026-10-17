# Ecosystem demo: `vercel/next.js`

This page is **not** presented as a current Maintainer Budget candidate cluster. It documents a public repository-specific review pattern that shows why durable repository memory matters and why agent instructions are a useful export target.

## Human review signal

In [PR #99195](https://github.com/vercel/next.js/pull/99195), maintainer `@gnoff` left a focused review comment:

> should we just use `@force-gate !dev` instead?

The author changed the PR accordingly and explained that the static gate is resolved at collection time rather than through the older mode-check pattern.

This is exactly the kind of knowledge a new contributor or coding agent is unlikely to infer from generic TypeScript/Jest knowledge alone: it is a convention of the Next.js test harness.

## Agent-instruction signal

In [PR #99582](https://github.com/vercel/next.js/pull/99582), Codex reviewed a test gate and explicitly cited `test/AGENTS.md` while arguing that a suite-level `@force-gate` would hide deployed behavior that should remain visible.

That is important for Maintainer Budget's product direction:

```text
historical maintainer feedback
        ↓
repository-specific rule
        ↓
AGENTS.md / scoped instructions
        ↓
agent review can apply the rule later
```

The Codex comment is **not** used as human training evidence by the alpha; bot feedback is ignored by default. It is included here only as public evidence that repository instructions can materially affect an agent review.

## Why this matters

Next.js has its own concepts such as `@gate`, `@force-gate`, deploy-mode behavior, and fixture lifecycle. A generic reviewer can understand JavaScript and Jest while still missing those local invariants.

Maintainer Budget's goal is to recover the recurring human feedback that reveals those invariants, preserve the original evidence, and let maintainers decide which ones deserve to become durable repository instructions.
